#!/usr/bin/env python3
"""
Decimal to Roman Numeral Converter

This module provides functionality to convert decimal numbers to Roman numerals.
Supports numbers from 1 to 3999.
"""

import sys
from typing import Union


def decimal_to_roman(num: int) -> str:
    """
    Convert a decimal number to Roman numeral.
    
    Args:
        num: Integer between 1 and 3999 inclusive
        
    Returns:
        Roman numeral representation as string
        
    Raises:
        ValueError: If num is not an integer or is outside valid range
    """
    if not isinstance(num, int):
        raise ValueError("Input must be an integer")
    
    if num < 1 or num > 3999:
        raise ValueError("Number must be between 1 and 3999")
    
    # Roman numeral mappings in descending order
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
    
    result = ""
    
    for i, value in enumerate(values):
        count = num // value
        if count > 0:
            result += numerals[i] * count
            num -= value * count
    
    return result


def main() -> None:
    """
    Main function to handle command line input and convert decimal to Roman numeral.
    """
    try:
        if len(sys.argv) != 2:
            print("Usage: python decimal_to_roman.py <number>")
            sys.exit(1)
        
        arg = sys.argv[1].strip()
        if not arg:
            raise ValueError("Empty argument provided")
        
        # Validate argument format before conversion
        if not arg.lstrip('-').isdigit():
            raise ValueError("Argument must be a valid integer")
        
        num = int(arg)
        roman = decimal_to_roman(num)
        print(f"{num} in Roman numerals is: {roman}")
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error occurred: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
