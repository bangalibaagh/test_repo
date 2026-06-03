#!/usr/bin/env python3
"""Script to convert decimal numbers to Roman numerals."""

import sys
from typing import Dict, List, Tuple


def decimal_to_roman(num: int) -> str:
    """Convert a decimal number to Roman numeral.
    
    Args:
        num: Integer between 1 and 3999 (inclusive)
        
    Returns:
        String representation of the Roman numeral
        
    Raises:
        ValueError: If number is not in valid range (1-3999)
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
        if count:
            result += numeral * count
            num -= value * count
    
    return result


def main() -> None:
    """Main function to handle user input and convert to Roman numeral."""
    if len(sys.argv) > 1:
        # If command line argument provided
        try:
            number = int(sys.argv[1])
            roman = decimal_to_roman(number)
            print(f"{number} in Roman numerals is: {roman}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Interactive mode
        try:
            user_input = input("Enter a decimal number (1-3999): ")
            number = int(user_input)
            roman = decimal_to_roman(number)
            print(f"{number} in Roman numerals is: {roman}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
