#!/usr/bin/env python3
"""Convert decimal numbers to Roman numerals."""

import sys


def decimal_to_roman(num: int) -> str:
    """Convert a decimal number to Roman numeral.
    
    Args:
        num: Integer between 1 and 3999
        
    Returns:
        Roman numeral representation as string
        
    Raises:
        ValueError: If number is out of valid range
    """
    if not 1 <= num <= 3999:
        raise ValueError("Number must be between 1 and 3999")
    
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    
    result = ""
    for i, value in enumerate(values):
        count = num // value
        result += symbols[i] * count
        num -= value * count
    
    return result


def main() -> None:
    """Main function for interactive mode."""
    print("Decimal to Roman Numeral Converter")
    print("Enter decimal numbers (1-3999) or Ctrl+C to exit")
    
    try:
        while True:
            try:
                user_input = input("Enter a number: ")
                num = int(user_input.strip())
                roman = decimal_to_roman(num)
                print(f"{num} = {roman}")
            except ValueError as e:
                print(f"Error: {e}")
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
