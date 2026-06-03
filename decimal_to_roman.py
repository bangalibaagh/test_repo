#!/usr/bin/env python3
"""
Decimal to Roman Numeral Converter

This script takes a decimal number as input and converts it to its Roman numeral equivalent.
Supports numbers from 1 to 3999.
"""

import sys
from typing import Dict, List, Tuple


def decimal_to_roman(num: int) -> str:
    """
    Convert a decimal number to Roman numeral.
    
    Args:
        num: Integer between 1 and 3999
        
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
    """
    Main function to handle user input and convert decimal to Roman numeral.
    """
    try:
        if len(sys.argv) > 1:
            # Take input from command line argument
            user_input = sys.argv[1]
        else:
            # Take input from user prompt
            user_input = input("Enter a decimal number (1-3999): ")
        
        # Convert input to integer
        try:
            decimal_num = int(user_input.strip())
        except ValueError:
            print("Error: Please enter a valid integer.")
            sys.exit(1)
        
        # Convert to Roman numeral
        roman_numeral = decimal_to_roman(decimal_num)
        print(f"{decimal_num} in Roman numerals is: {roman_numeral}")
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
