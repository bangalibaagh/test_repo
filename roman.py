#!/usr/bin/env python3
"""Script to convert decimal numbers to Roman numerals."""

import sys
from typing import Optional


def decimal_to_roman(num: int) -> str:
    """Convert a decimal number to Roman numeral.
    
    Args:
        num: Integer between 1 and 3999 (inclusive)
        
    Returns:
        Roman numeral representation as string
        
    Raises:
        ValueError: If number is out of valid range
    """
    if not isinstance(num, int) or num < 1 or num > 3999:
        raise ValueError("Number must be an integer between 1 and 3999")
    
    # Roman numeral mappings in descending order
    values = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    
    result = ''
    for value, numeral in values:
        count = num // value
        if count:
            result += numeral * count
            num -= value * count
    
    return result


def get_user_input() -> Optional[int]:
    """Get and validate user input.
    
    Returns:
        Valid integer or None if invalid input
    """
    try:
        user_input = input("Enter a decimal number (1-3999): ").strip()
        return int(user_input)
    except (ValueError, EOFError, KeyboardInterrupt):
        return None


def main() -> None:
    """Main function to handle command-line execution."""
    # Check if number provided as command-line argument
    if len(sys.argv) == 2:
        try:
            num = int(sys.argv[1])
            roman = decimal_to_roman(num)
            print(f"{num} = {roman}")
            return
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif len(sys.argv) > 2:
        print("Usage: python roman.py [number]", file=sys.stderr)
        sys.exit(1)
    
    # Interactive mode
    print("Roman Numeral Converter")
    print("Enter a number between 1 and 3999 (or Ctrl+C to exit)")
    
    while True:
        try:
            num = get_user_input()
            if num is None:
                print("Invalid input. Please enter a valid integer.")
                continue
            
            roman = decimal_to_roman(num)
            print(f"{num} = {roman}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
