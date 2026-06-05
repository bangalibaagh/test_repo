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
        ValueError: If number is not in valid range (1-3999)
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
        Valid integer or None if input is invalid
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
            print(f"{num} in Roman numerals is: {roman}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Interactive mode
        print("Decimal to Roman Numeral Converter")
        print("Enter a number between 1 and 3999 (or Ctrl+C to quit)")
        
        while True:
            try:
                num = get_user_input()
                if num is None:
                    print("Invalid input. Please enter a valid integer.")
                    continue
                
                roman = decimal_to_roman(num)
                print(f"{num} in Roman numerals is: {roman}")
                
                # Ask if user wants to continue
                continue_input = input("\nConvert another number? (y/n): ").strip().lower()
                if continue_input not in ['y', 'yes']:
                    break
                    
            except ValueError as e:
                print(f"Error: {e}")
                # Continue the loop after handling ValueError
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break


if __name__ == "__main__":
    main()
