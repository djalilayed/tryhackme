# script for tryhackme room Orcam part of Industrial Intrusion CTF https://tryhackme.com/room/industrial-intrusion
# script with assist of Claudi AI
# YouTube video walk throug: https://youtu.be/uGhuElHm1Ys

#!/usr/bin/env python3
"""
VBA Macro XOR Decoder - Comprehensive Analysis
Tests different XOR key interpretations to understand the actual decoding
"""

def decode_with_single_key(encoded_payload, key_char):
    """Decode using single character XOR (VBA Asc() behavior)"""
    key_byte = ord(key_char)
    decoded = []
    for byte_val in encoded_payload:
        decoded.append(byte_val ^ key_byte)
    return decoded

def decode_with_rotating_key(encoded_payload, key_string):
    """Decode using rotating multi-character XOR key"""
    decoded = []
    for i, byte_val in enumerate(encoded_payload):
        key_byte = ord(key_string[i % len(key_string)])
        decoded.append(byte_val ^ key_byte)
    return decoded

def analyze_decoding_quality(decoded_payload, method_name):
    """Analyze how 'good' a decoding is based on printable characters"""
    printable_count = sum(1 for b in decoded_payload if 32 <= b <= 126)
    printable_ratio = printable_count / len(decoded_payload)
    
    # Look for common strings that indicate successful decoding
    ascii_str = ''.join([chr(x) if 32 <= x <= 126 else '.' for x in decoded_payload])
    
    indicators = {
        'net user': 'Windows user management',
        'cmd': 'Command execution',
        'powershell': 'PowerShell',
        'http': 'Network communication',
        'kernel32': 'Windows API',
        'CreateProcess': 'Process creation',
        'VirtualAlloc': 'Memory allocation'
    }
    
    found_indicators = []
    for indicator, description in indicators.items():
        if indicator.lower() in ascii_str.lower():
            found_indicators.append((indicator, description))
    
    return {
        'method': method_name,
        'printable_ratio': printable_ratio,
        'printable_count': printable_count,
        'total_bytes': len(decoded_payload),
        'indicators': found_indicators,
        'ascii_preview': ascii_str[:200],
        'full_ascii': ascii_str
    }

def test_vba_asc_function():
    """Test what VBA's Asc() function actually returns"""
    print("="*60)
    print("VBA Asc() FUNCTION BEHAVIOR TEST")
    print("="*60)
    
    test_strings = ["l33t", "l", "test", "abcd"]
    
    print("In VBA, Asc() only returns the ASCII value of the FIRST character:")
    for s in test_strings:
        first_char_ascii = ord(s[0])
        print(f"  Asc('{s}') = {first_char_ascii} ('{s[0]}')")
    
    print(f"\nSo in the macro: Asc('l33t') = {ord('l')} (just the 'l')")
    print()

def main():
    print("VBA Macro XOR Decoder - Comprehensive Analysis")
    print("="*50)
    
    # Original encoded payload
    encoded_payload = [
        144, 219, 177, 116, 108, 51, 83, 253, 137, 2, 243, 16, 231, 99, 3, 255, 62, 63, 184, 38, 120, 184, 65, 92, 99, 132, 121, 82, 93, 204, 159, 72, 13, 79, 49, 88, 76, 242, 252, 121, 109, 244, 209, 134, 62, 100, 184, 38, 124, 184, 121, 72, 231, 127, 34, 12, 143, 123, 50, 165, 61, 184, 106, 84, 109, 224, 184, 61, 116, 208, 9, 61, 231, 7, 184, 117, 186, 2, 204, 216, 173,
        252, 62, 117, 171, 11, 211, 1, 154, 48, 78, 140, 87, 78, 23, 1, 136, 107, 184, 44, 72, 50, 224, 18, 231, 63, 120, 255, 52, 47, 50, 167, 231, 55, 184, 117, 188, 186, 119, 80, 72, 104, 104, 21, 53, 105, 98, 139, 140, 108, 108, 46, 231, 33, 216, 249, 49, 89, 50, 249, 233, 129, 51, 116, 108, 99, 91, 69, 231, 92, 180, 139, 185, 136, 211, 105, 70, 57, 91, 210, 249,
        142, 174, 139, 185, 15, 53, 8, 102, 179, 200, 148, 25, 54, 136, 51, 127, 65, 92, 30, 108, 96, 204, 161, 2, 86, 71, 84, 25, 64, 86, 6, 76, 82, 87, 25, 5, 93, 90, 7, 24, 65, 65, 21, 24, 92, 65, 84, 58, 118, 91, 58, 9, 3, 101, 70, 33, 100, 75, 18, 56, 102, 113, 48, 15, 89, 113, 77, 76, 28, 82, 16, 8, 19, 28, 45, 76, 21, 19, 26, 9,
        71, 19, 24, 3, 80, 82, 24, 11, 65, 92, 1, 28, 19, 82, 16, 1, 90, 93, 29, 31, 71, 65, 21, 24, 92, 65, 7, 76, 82, 87, 25, 5, 93, 90, 7, 24, 65, 65, 21, 24, 92, 65, 84, 67, 82, 87, 16, 108
    ]
    
    print(f"Encoded payload length: {len(encoded_payload)} bytes")
    
    # Test VBA Asc() behavior
    test_vba_asc_function()
    
    # Test different decoding methods
    methods_to_test = [
        ("Single 'l' (VBA Asc behavior)", lambda: decode_with_single_key(encoded_payload, 'l')),
        ("Rotating 'l33t'", lambda: decode_with_rotating_key(encoded_payload, 'l33t')),
        ("Single '3'", lambda: decode_with_single_key(encoded_payload, '3')),
        ("Rotating 'l3'", lambda: decode_with_rotating_key(encoded_payload, 'l3')),
        ("Single 't'", lambda: decode_with_single_key(encoded_payload, 't')),
    ]
    
    results = []
    
    print("="*60)
    print("TESTING DIFFERENT DECODING METHODS")
    print("="*60)
    
    for method_name, decode_func in methods_to_test:
        print(f"\n[+] Testing: {method_name}")
        decoded = decode_func()
        analysis = analyze_decoding_quality(decoded, method_name)
        results.append(analysis)
        
        print(f"    Printable chars: {analysis['printable_count']}/{analysis['total_bytes']} ({analysis['printable_ratio']:.1%})")
        print(f"    Indicators found: {len(analysis['indicators'])}")
        for indicator, desc in analysis['indicators']:
            print(f"      - {indicator}: {desc}")
        print(f"    Preview: {analysis['ascii_preview'][:100]}...")
    
    # Find the best result
    best_result = max(results, key=lambda x: (len(x['indicators']), x['printable_ratio']))
    
    print("\n" + "="*60)
    print("BEST DECODING RESULT")
    print("="*60)
    
    print(f"Method: {best_result['method']}")
    print(f"Quality: {best_result['printable_ratio']:.1%} printable characters")
    print(f"Indicators: {len(best_result['indicators'])} found")
    print()
    
    print("Full ASCII output:")
    print("-" * 40)
    print(best_result['full_ascii'])
    print("-" * 40)
    
    # Explain why partial decoding occurs
    print("\n" + "="*60)
    print("WHY PARTIAL DECODING OCCURS")
    print("="*60)
    
    print("""
The partial decoding happens because:

1. SHELLCODE STRUCTURE: The payload contains both:
   - Binary shellcode (assembly instructions) - appears as dots/garbage
   - Embedded strings (commands, URLs, etc.) - appears as readable text

2. MIXED CONTENT: Shellcode typically has:
   - Machine code instructions (non-printable bytes)
   - API function names and strings (printable)
   - Memory addresses and offsets (often non-printable)

3. ENCODING PURPOSE: The XOR encoding is meant to:
   - Bypass antivirus signature detection
   - Hide the payload during static analysis
   - Obfuscate the actual functionality

The readable parts you see (like 'net user administrrator...') are the 
PAYLOAD COMMANDS that the shellcode will execute, embedded within the 
binary shellcode structure.
    """)
    
    # Show hex dump of best result for further analysis
    print("\n" + "="*60)
    print("HEX DUMP FOR FURTHER ANALYSIS")
    print("="*60)
    
    # Get the decoded bytes for best method
    if best_result['method'] == "Rotating 'l33t'":
        best_decoded = decode_with_rotating_key(encoded_payload, 'l33t')
    else:
        best_decoded = decode_with_single_key(encoded_payload, 'l')
    
    print("Hex dump (first 200 bytes):")
    for i in range(0, min(200, len(best_decoded)), 16):
        hex_part = ' '.join(f'{b:02X}' for b in best_decoded[i:i+16])
        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in best_decoded[i:i+16])
        print(f"{i:04X}: {hex_part:<48} {ascii_part}")
    
    print(f"\n[+] Analysis complete!")
    print(f"[+] Best method appears to be: {best_result['method']}")
    
    # Save the best result
    try:
        with open('best_decoded_shellcode.bin', 'wb') as f:
            f.write(bytes(best_decoded))
        print(f"[+] Saved best result to: best_decoded_shellcode.bin")
    except Exception as e:
        print(f"[-] Error saving: {e}")

if __name__ == "__main__":
    main()
