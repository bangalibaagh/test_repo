#!/usr/bin/env python3
"""Roman numeral conversion script.

Converts decimal integers to Roman numeral representation.
"""

from typing import Dict, List, Tuple


def decimal_to_roman(num: int) -> str:
    """Convert a decimal integer to Roman numeral.
    
    Args:
        num: Integer between 1 and 3999 (inclusive)
        
    Returns:
        String representation of the Roman numeral
        
    Raises:
        ValueError: If num is not in valid range [1, 3999]
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
    """Main function for command line usage."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python roman.py <decimal_number>")
        print("Convert a decimal number (1-3999) to Roman numeral")
        sys.exit(1)
    
    try:
        number = int(sys.argv[1])
        roman = decimal_to_roman(number)
        print(f"{number} = {roman}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
