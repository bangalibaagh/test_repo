#!/usr/bin/env python3
"""Roman numeral converter script.

Converts decimal numbers to Roman numerals.
"""

import sys
from typing import Dict, List, Tuple


def decimal_to_roman(num: int) -> str:
    """Convert a decimal number to Roman numeral.
    
    Args:
        num: Integer between 1 and 3999 (inclusive)
        
    Returns:
        Roman numeral representation as string
        
    Raises:
        ValueError: If number is out of valid range (1-3999)
    """
    if not isinstance(num, int) or num < 1 or num > 3999:
        raise ValueError("Number must be an integer between 1 and 3999")
    
    # Roman numeral mappings in descending order
    roman_numerals: List[Tuple[int, str]] = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I')
    ]
    
    result = ""
    
    for value, numeral in roman_numerals:
        count = num // value
        if count > 0:
            result += numeral * count
            num -= value * count
    
    return result


def main() -> None:
    """Main function to handle command-line input and output."""
    if len(sys.argv) != 2:
        print("Usage: python roman.py <decimal_number>", file=sys.stderr)
        print("Convert a decimal number (1-3999) to Roman numerals", file=sys.stderr)
        sys.exit(1)
    
    try:
        decimal_input = int(sys.argv[1])
        roman_output = decimal_to_roman(decimal_input)
        print(roman_output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
