#!/usr/bin/env python3
"""Roman numeral converter script.

Converts decimal numbers to Roman numerals.
"""

import argparse
import sys
from typing import Dict, List, Tuple


def decimal_to_roman(num: int) -> str:
    """Convert a decimal number to Roman numeral.
    
    Args:
        num: Integer between 1 and 3999 inclusive
        
    Returns:
        Roman numeral string representation
        
    Raises:
        ValueError: If number is out of valid range (1-3999)
    """
    if not isinstance(num, int) or num < 1 or num > 3999:
        raise ValueError("Number must be an integer between 1 and 3999")
    
    # Roman numeral mappings in descending order
    values: List[Tuple[int, str]] = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    
    result = ""
    for value, numeral in values:
        count = num // value
        if count:
            result += numeral * count
            num -= value * count
    
    return result


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert decimal numbers to Roman numerals",
        prog="roman"
    )
    parser.add_argument(
        "number",
        type=int,
        help="Decimal number to convert (1-3999)"
    )
    
    try:
        args = parser.parse_args()
        roman_numeral = decimal_to_roman(args.number)
        print(roman_numeral)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
