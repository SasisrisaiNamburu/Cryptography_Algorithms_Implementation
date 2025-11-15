#!/usr/bin/env python3
"""
caesar_cipher.py
Simple Caesar cipher implementation with CLI.

Usage examples:
  python caesar_cipher.py -e 3 "Hello, World!"
  python caesar_cipher.py -d 3 "Khoor, Zruog!"
  python caesar_cipher.py -e 5 -f samples/sample_text.txt
"""

import argparse
import sys
from pathlib import Path
from typing import Tuple

def caesar_shift_char(ch: str, key: int) -> str:
    """Shift a single character by key positions; preserve case; non-alpha unchanged."""
    if 'a' <= ch <= 'z':
        base = ord('a')
        return chr((ord(ch) - base + key) % 26 + base)
    if 'A' <= ch <= 'Z':
        base = ord('A')
        return chr((ord(ch) - base + key) % 26 + base)
    return ch

def caesar_transform(text: str, key: int) -> str:
    """Apply Caesar shift to full string."""
    return ''.join(caesar_shift_char(ch, key) for ch in text)

def encrypt(text: str, key: int) -> str:
    return caesar_transform(text, key)

def decrypt(text: str, key: int) -> str:
    return caesar_transform(text, -key)

def parse_args(argv: list) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Caesar cipher — encrypt or decrypt text.")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', action='store_true', help='Encrypt mode')
    group.add_argument('-d', '--decrypt', action='store_true', help='Decrypt mode')
    p.add_argument('key', type=int, help='Integer shift key (e.g., 3)')
    p.add_argument('text', nargs='?', help='Text to transform (if not provided, use -f)')
    p.add_argument('-f', '--file', type=Path, help='Path to a text file to read input from')
    p.add_argument('-o', '--output', type=Path, help='Optional output file (writes result)')
    return p.parse_args(argv)

def main(argv: list):
    args = parse_args(argv)

    if args.file:
        if not args.file.exists():
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        text = args.file.read_text(encoding='utf-8')
    elif args.text:
        text = args.text
    else:
        print("Error: either provide TEXT or use -f/--file to read a file.", file=sys.stderr)
        sys.exit(2)

    key = args.key % 26
    if args.encrypt:
        result = encrypt(text, key)
    else:
        result = decrypt(text, key)

    if args.output:
        args.output.write_text(result, encoding='utf-8')
        print(f"Result written to {args.output}")
    else:
        print(result)

if __name__ == '__main__':
    main(sys.argv[1:])
