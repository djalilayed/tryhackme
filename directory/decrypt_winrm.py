# original script / credit to https://gist.github.com/jborean93/d6ff5e87f8a9f5cb215cd49826523045/
# Copyright: (c) 2020 Jordan Borean (@jborean93) <jborean93@gmail.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

# script updated by Claudi AI to fix some errors on python 3
# script used on tryhackme room https://tryhackme.com/room/directorydfirroom
# YouTube video walk through: https://youtu.be/sET2aPr2CIg
# Key Features Maintained:
# Same core cryptographic logic (NTLM, RC4, MD5, HMAC)
# Compatible with existing capture files
# Same decryption algorithm
# Backward compatibility with original functionality
# New Features:
# Better error messages and debugging
# Structured logging output
# Live capture support with proper interface
# Improved MIME parsing
# Better XML formatting
# Resource cleanup
# More robust packet processing

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modern WinRM Traffic Decoder

A modernized script to read Wireshark captures (.pcapng) for WinRM exchanges 
and decrypt the messages. Supports NTLM authentication with improved error 
handling and modern Python features.

Copyright: (c) 2020 Jordan Borean (@jborean93) <jborean93@gmail.com>
MIT License (see LICENSE or https://opensource.org/licenses/MIT)
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import os
import re
import struct
import xml.dom.minidom
from pathlib import Path
from typing import Optional, List, Tuple, Union
import logging

import pyshark
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

# MD4 implementation using PyCryptodome
try:
    from Crypto.Hash import MD4 as CryptoMD4
    MD4_AVAILABLE = True
except ImportError:
    MD4_AVAILABLE = False
    logging.warning("PyCryptodome not available. Install with: pip install pycryptodome")

try:
    import argcomplete
    ARGCOMPLETE_AVAILABLE = True
except ImportError:
    ARGCOMPLETE_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Compiled regex patterns for better performance
BOUNDARY_PATTERN = re.compile(r"boundary=[\"']?([^\"';]+)[\"']?", re.IGNORECASE)
MIME_CONTENT_TYPE_PATTERN = re.compile(rb"\t?Content-Type: application/octet-stream\r?\n", re.IGNORECASE)


class WinRMDecryptionError(Exception):
    """Custom exception for WinRM decryption errors."""
    pass


class SecurityContext:
    """Manages NTLM security context for WinRM traffic decryption."""
    
    def __init__(self, port: int, nt_hash: bytes) -> None:
        self.port = port
        self.tokens: List[bytes] = []
        self.nt_hash = nt_hash
        self.complete = False

        # NTLM session parameters
        self.key_exch = False
        self.session_key: Optional[bytes] = None
        self.sign_key_initiate: Optional[bytes] = None
        self.sign_key_accept: Optional[bytes] = None
        self.seal_handle_initiate = None
        self.seal_handle_accept = None

        # Sequence numbers for message integrity
        self._initiate_seq_counter = 0
        self._accept_seq_counter = 0

    @property
    def initiate_seq_no(self) -> int:
        """Get next initiate sequence number."""
        val = self._initiate_seq_counter
        self._initiate_seq_counter += 1
        return val

    @property
    def accept_seq_no(self) -> int:
        """Get next accept sequence number."""
        val = self._accept_seq_counter
        self._accept_seq_counter += 1
        return val

    def add_token(self, token: bytes) -> None:
        """Add an NTLM token and process if it's the final authentication message."""
        self.tokens.append(token)

        if token.startswith(b"NTLMSSP\x00\x03"):
            self._process_type3_message(token)

    def _process_type3_message(self, token: bytes) -> None:
        """Process NTLM Type 3 (Authentication) message to derive session keys."""
        try:
            # Extract authentication fields
            nt_challenge = self._get_auth_field(20, token)
            if not nt_challenge:
                raise WinRMDecryptionError("Failed to extract NT challenge")
                
            b_domain = self._get_auth_field(28, token) or b""
            b_username = self._get_auth_field(36, token) or b""
            encrypted_random_session_key = self._get_auth_field(52, token)
            flags = struct.unpack("<I", token[60:64])[0]

            # Determine encoding based on NTLM flags
            encoding = "utf-16-le" if flags & 0x00000001 else "windows-1252"
            domain = b_domain.decode(encoding)
            username = b_username.decode(encoding)

            # Derive the session key using NTLM cryptographic functions
            nt_proof_str = nt_challenge[:16]
            response_key_nt = self._hmac_md5(
                self.nt_hash, 
                (username.upper() + domain).encode("utf-16-le")
            )
            key_exchange_key = self._hmac_md5(response_key_nt, nt_proof_str)
            self.key_exch = bool(flags & 0x40000000)

            if self.key_exch and (flags & (0x00000020 | 0x00000010)):
                if not encrypted_random_session_key:
                    raise WinRMDecryptionError("Missing encrypted session key")
                self.session_key = self._rc4_decrypt(key_exchange_key, encrypted_random_session_key)
            else:
                self.session_key = key_exchange_key

            # Derive signing and sealing keys
            self.sign_key_initiate = self._derive_sign_key("initiate")
            self.sign_key_accept = self._derive_sign_key("accept")
            self.seal_handle_initiate = self._init_rc4_cipher(self._derive_seal_key("initiate"))
            self.seal_handle_accept = self._init_rc4_cipher(self._derive_seal_key("accept"))
            self.complete = True
            
            logger.info(f"NTLM authentication completed for port {self.port}")
            
        except Exception as e:
            raise WinRMDecryptionError(f"Failed to process NTLM Type 3 message: {e}") from e

    def unwrap_initiate(self, data: bytes) -> bytes:
        """Decrypt and verify data from client to server."""
        return self._unwrap_data(
            self.seal_handle_initiate, 
            self.sign_key_initiate, 
            self.initiate_seq_no, 
            data
        )

    def unwrap_accept(self, data: bytes) -> bytes:
        """Decrypt and verify data from server to client."""
        return self._unwrap_data(
            self.seal_handle_accept, 
            self.sign_key_accept, 
            self.accept_seq_no, 
            data
        )

    def _unwrap_data(self, cipher_handle, sign_key: bytes, seq_no: int, data: bytes) -> bytes:
        """Decrypt and verify message integrity."""
        if len(data) < 20:
            raise WinRMDecryptionError("Invalid message format: too short")
            
        header = data[4:20]
        encrypted_data = data[20:]
        
        # Decrypt the data
        decrypted_data = cipher_handle.update(encrypted_data)
        
        # Verify message integrity
        seq_bytes = struct.pack("<I", seq_no)
        expected_checksum = self._hmac_md5(sign_key, seq_bytes + decrypted_data)[:8]
        
        if self.key_exch:
            expected_checksum = cipher_handle.update(expected_checksum)
            
        expected_header = b"\x01\x00\x00\x00" + expected_checksum + seq_bytes

        if header != expected_header:
            raise WinRMDecryptionError("Message signature verification failed")

        return decrypted_data

    def _get_auth_field(self, offset: int, token: bytes) -> Optional[bytes]:
        """Extract authentication field from NTLM token."""
        if len(token) < offset + 8:
            return None
            
        field_len = struct.unpack("<H", token[offset:offset + 2])[0]
        if field_len == 0:
            return None
            
        field_offset = struct.unpack("<I", token[offset + 4:offset + 8])[0]
        if field_offset + field_len > len(token):
            return None
            
        return token[field_offset:field_offset + field_len]

    @staticmethod
    def _hmac_md5(key: bytes, data: bytes) -> bytes:
        """Compute HMAC-MD5."""
        return hmac.new(key, data, digestmod=hashlib.md5).digest()

    def _derive_seal_key(self, usage: str) -> bytes:
        """Derive sealing key for encryption."""
        direction = b"client-to-server" if usage == "initiate" else b"server-to-client"
        return self._md5(
            self.session_key + 
            b"session key to %s sealing key magic constant\x00" % direction
        )

    def _derive_sign_key(self, usage: str) -> bytes:
        """Derive signing key for message authentication."""
        direction = b"client-to-server" if usage == "initiate" else b"server-to-client"
        return self._md5(
            self.session_key + 
            b"session key to %s signing key magic constant\x00" % direction
        )

    @staticmethod
    def _init_rc4_cipher(key: bytes):
        """Initialize RC4 cipher with given key."""
        arc4 = algorithms.ARC4(key)
        return Cipher(arc4, mode=None, backend=default_backend()).encryptor()

    @staticmethod
    def _rc4_decrypt(key: bytes, data: bytes) -> bytes:
        """Decrypt data using RC4."""
        return SecurityContext._init_rc4_cipher(key).update(data)

    @staticmethod
    def _md5(data: bytes) -> bytes:
        """Compute MD5 hash."""
        return hashlib.md5(data).digest()


class WinRMDecoder:
    """Main class for decoding WinRM traffic."""
    
    def __init__(self, nt_hash: bytes, target_port: int = 5985):
        self.nt_hash = nt_hash
        self.target_port = target_port
        self.contexts: List[SecurityContext] = []

    def process_capture_file(self, file_path: Union[str, Path]) -> None:
        """Process a pcapng capture file."""
        file_path = Path(file_path).expanduser().resolve()
        
        if not file_path.exists():
            raise FileNotFoundError(f"Capture file not found: {file_path}")
        
        logger.info(f"Processing capture file: {file_path}")
        
        display_filter = f"http and tcp.port == {self.target_port}"
        
        try:
            with pyshark.FileCapture(str(file_path), display_filter=display_filter) as capture:
                packet_count = 0
                for packet in capture:
                    self._process_packet(packet)
                    packet_count += 1
                    
            logger.info(f"Processed {packet_count} packets")
            
        except Exception as e:
            logger.error(f"Failed to process capture: {e}")
            raise

    def process_live_capture(self, interface: str) -> None:
        """Process live network traffic."""
        logger.info(f"Starting live capture on interface: {interface}")
        
        display_filter = f"http and tcp.port == {self.target_port}"
        
        try:
            capture = pyshark.LiveCapture(
                interface=interface,
                display_filter=display_filter
            )
            
            for packet in capture.sniff_continuously():
                self._process_packet(packet)
                
        except KeyboardInterrupt:
            logger.info("Live capture stopped by user")
        except Exception as e:
            logger.error(f"Live capture failed: {e}")
            raise

    def _process_packet(self, packet) -> None:
        """Process individual network packet."""
        try:
            source_port = int(packet.tcp.srcport)
            unique_port = source_port if source_port != self.target_port else int(packet.tcp.dstport)

            # Process NTLM authentication tokens
            auth_token = self._extract_auth_token(packet)
            if auth_token:
                context = self._handle_auth_token(auth_token, unique_port)
                
            # Process encrypted WinRM messages
            if hasattr(packet.http, 'file_data'):
                self._process_winrm_message(packet, unique_port, source_port)
                
        except Exception as e:
            logger.error(f"Failed to process packet {getattr(packet, 'number', 'unknown')}: {e}")

    def _extract_auth_token(self, packet) -> Optional[bytes]:
        """Extract NTLM authentication token from HTTP headers."""
        try:
            if hasattr(packet.http, "authorization"):
                b64_token = packet.http.authorization.split(" ", 1)[1]
                return base64.b64decode(b64_token)
                
            elif hasattr(packet.http, "www_authenticate"):
                auth_parts = packet.http.www_authenticate.split(" ", 1)
                if len(auth_parts) > 1:
                    return base64.b64decode(auth_parts[1])
                    
        except (IndexError, ValueError) as e:
            logger.debug(f"Failed to extract auth token: {e}")
            
        return None

    def _handle_auth_token(self, token: bytes, port: int) -> Optional[SecurityContext]:
        """Handle NTLM authentication token."""
        if not token.startswith(b"NTLMSSP\x00"):
            return None

        if token.startswith(b"NTLMSSP\x00\x01"):
            # Type 1: Negotiate message - create new context
            context = SecurityContext(port, self.nt_hash)
            self.contexts.append(context)
            logger.debug(f"Created new NTLM context for port {port}")
            
        else:
            # Type 2 or 3: Find existing context
            matching_contexts = [c for c in self.contexts if c.port == port]
            if not matching_contexts:
                logger.warning(f"No existing NTLM context for port {port}")
                return None
            context = matching_contexts[-1]

        context.add_token(token)
        return context

    def _process_winrm_message(self, packet, unique_port: int, source_port: int) -> None:
        """Process and decrypt WinRM message data."""
        context = self._find_context_by_port(unique_port)
        if not context:
            logger.debug(f"No context found for port {unique_port}")
            return

        if not context.complete:
            logger.debug("Cannot decrypt - NTLM context not complete")
            return

        try:
            file_data = packet.http.file_data.binary_value
            messages = self._unpack_multipart_message(packet.http.content_type, file_data)

            # Determine decryption function based on message direction
            decrypt_func = (context.unwrap_accept if source_port == self.target_port 
                          else context.unwrap_initiate)

            decrypted_messages = []
            for expected_length, encrypted_data in messages:
                decrypted = decrypt_func(encrypted_data)
                
                if len(decrypted) != expected_length:
                    raise WinRMDecryptionError(
                        f"Length mismatch: expected {expected_length}, got {len(decrypted)}"
                    )
                
                xml_content = self._format_xml(decrypted.decode("utf-8"))
                decrypted_messages.append(xml_content)

            # Output results
            combined_messages = "\n".join(decrypted_messages)
            self._output_decrypted_message(packet, combined_messages)

        except Exception as e:
            logger.error(f"Failed to decrypt WinRM message: {e}")

    def _find_context_by_port(self, port: int) -> Optional[SecurityContext]:
        """Find security context by port number."""
        matching_contexts = [c for c in self.contexts if c.port == port]
        return matching_contexts[0] if matching_contexts else None

    def _unpack_multipart_message(self, content_type: str, data: bytes) -> List[Tuple[int, bytes]]:
        """Unpack multipart MIME message containing encrypted WinRM data."""
        boundary_match = BOUNDARY_PATTERN.search(content_type)
        if not boundary_match:
            raise ValueError("Unable to parse MIME boundary from content type")

        boundary = boundary_match.group(1)
        
        # Handle Exchange's non-compliant boundary format
        boundary_pattern = re.compile(
            (r"--\s*" + re.escape(boundary) + r"\r\n").encode()
        )
        
        parts = boundary_pattern.split(data)
        parts = [part for part in parts if part.strip()]

        messages = []
        for i in range(0, len(parts), 2):
            if i + 1 >= len(parts):
                break
                
            header = parts[i].strip()
            payload = parts[i + 1]

            # Extract content length
            try:
                length = int(header.split(b"Length=")[1].split()[0])
            except (IndexError, ValueError):
                logger.warning("Failed to parse message length")
                continue

            # Clean up payload
            end_boundary_pattern = re.compile(
                (r"--\s*" + re.escape(boundary) + r"--\r\n$").encode()
            )
            payload = end_boundary_pattern.sub(b"", payload)
            payload = MIME_CONTENT_TYPE_PATTERN.sub(b"", payload)

            messages.append((length, payload))

        return messages

    @staticmethod
    def _format_xml(xml_string: str) -> str:
        """Format XML string for better readability."""
        try:
            dom = xml.dom.minidom.parseString(xml_string)
            return dom.toprettyxml(indent="  ")
        except Exception:
            # Return original if parsing fails
            return xml_string

    @staticmethod
    def _output_decrypted_message(packet, message: str) -> None:
        """Output decrypted message with packet information."""
        print(f"\n{'='*80}")
        print(f"Packet: {packet.number} | Time: {packet.sniff_time.isoformat()}")
        print(f"Source: {packet.ip.src_host} | Destination: {packet.ip.dst_host}")
        print(f"{'='*80}")
        print(message)
        print(f"{'='*80}\n")


def compute_nt_hash(password: str) -> bytes:
    """Compute NT hash from password using MD4."""
    if not MD4_AVAILABLE:
        raise ImportError(
            "PyCryptodome is required for MD4 support. Install with: pip install pycryptodome"
        )
    
    utf16_password = password.encode('utf-16le')
    return CryptoMD4.new(utf16_password).digest()


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Decrypt WinRM traffic from Wireshark captures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -p 'Password123!' capture.pcapng
  %(prog)s -n 'A1B2C3D4E5F6789...' capture.pcapng --port 5986
  %(prog)s -p 'Password123!' --live-capture eth0
        """
    )

    parser.add_argument(
        "path",
        type=str,
        help="Path to pcapng file or network interface name (with --live-capture)"
    )

    parser.add_argument(
        "--live-capture",
        action="store_true",
        help="Perform live capture on specified network interface"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=5985,
        help="WinRM port to monitor (default: 5985)"
    )

    # Mutually exclusive authentication options
    auth_group = parser.add_mutually_exclusive_group(required=True)
    
    auth_group.add_argument(
        "-p", "--password",
        help="Password for NTLM authentication"
    )
    
    auth_group.add_argument(
        "-n", "--nt-hash",
        help="NT hash for NTLM authentication (hex format)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    if ARGCOMPLETE_AVAILABLE:
        argcomplete.autocomplete(parser)

    return parser.parse_args()


def main() -> None:
    """Main program entry point."""
    try:
        args = parse_arguments()
        
        # Configure logging level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Derive NT hash
        if args.password:
            nt_hash = compute_nt_hash(args.password)
            logger.info("Using password authentication")
        else:
            try:
                nt_hash = base64.b16decode(args.nt_hash.upper())
                logger.info("Using NT hash authentication")
            except ValueError as e:
                logger.error(f"Invalid NT hash format: {e}")
                return

        # Initialize decoder
        decoder = WinRMDecoder(nt_hash, args.port)
        
        # Process traffic
        if args.live_capture:
            decoder.process_live_capture(args.path)
        else:
            decoder.process_capture_file(args.path)
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if args.verbose:
            logger.exception("Detailed error information:")


if __name__ == "__main__":
    main()
