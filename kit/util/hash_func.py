#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hash utilities for generating hash codes and checksums
"""


def simple_hash(string, case_sensitive=True):
    """
    Generates a simple hash code from a string

    Args:
        string (str): The string to hash
        case_sensitive (bool, optional): Whether the hash should be case sensitive. Defaults to True.

    Returns:
        int: A numeric hash code
    """
    if not string:
        return 0

    # Convert to lowercase if not case sensitive
    processed_str = string if case_sensitive else string.lower()

    hash_val = 0
    for char in processed_str:
        char_code = ord(char)
        hash_val = ((hash_val << 5) - hash_val) + char_code
        hash_val = hash_val & 0xFFFFFFFF  # Convert to 32bit integer using bitwise AND

    return abs(hash_val)


def hash_code(value):
    """
    Generates a hash code from any Python value (string, number, object, list)

    Args:
        value: The value to hash

    Returns:
        int: A numeric hash code
    """
    if value is None:
        return 0

    if isinstance(value, str):
        return simple_hash(value)

    if isinstance(value, (int, float)):
        return simple_hash(str(value))

    if isinstance(value, bool):
        return 1 if value else 0

    if isinstance(value, list):
        return simple_hash('|'.join(str(hash_code(item)) for item in value))

    if isinstance(value, dict):
        # Sort keys to ensure consistent hashing regardless of property order
        sorted_keys = sorted(value.keys())
        key_value_pairs = [f"{key}:{hash_code(value[key])}" for key in sorted_keys]
        return simple_hash('|'.join(key_value_pairs))

    # Fall back to string conversion for other types
    return simple_hash(str(value))


def hex_hash(value, length=8):
    """
    Generates a hexadecimal hash string (MD5-like but simpler)

    Args:
        value: The value to hash
        length (int, optional): The desired length of the hex string. Defaults to 8.

    Returns:
        str: A hexadecimal hash string
    """
    hash_val = hash_code(value)
    # Convert to hex string and remove '0x' prefix
    hex_string = format(hash_val, 'x')

    # Ensure the hex string is at least the requested length
    hex_string = hex_string.zfill(length)

    # Trim if longer than requested length
    return hex_string[:length]


def hash_equals(value1, value2):
    """
    Check if two values have the same hash

    Args:
        value1: First value to compare
        value2: Second value to compare

    Returns:
        bool: True if the hash codes are the same
    """
    return hash_code(value1) == hash_code(value2)

