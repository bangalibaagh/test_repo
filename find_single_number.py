#!/usr/bin/env python3
"""
Script to find the single number that appears once in a list where all other numbers appear twice.

Usage: python find_single_number.py "1,2,3,2,1"
"""

import sys


def find_single_number(nums):
    """
    Find the single number that appears once in a list where all other numbers appear twice.
    
    Args:
        nums: List of integers
        
    Returns:
        int: The number that appears exactly once
        
    Raises:
        ValueError: If input is empty or doesn't contain exactly one unique number
    """
    if not nums:
        raise ValueError("Input list cannot be empty")
    
    # Use XOR to find the single number
    # XOR of two same numbers is 0
    # XOR of any number with 0 is the number itself
    result = 0
    for num in nums:
        result ^= num
    
    return result


def parse_input(input_str):
    """
    Parse comma-separated string of numbers into a list of integers.
    
    Args:
        input_str: String containing comma-separated numbers
        
    Returns:
        list: List of integers
        
    Raises:
        ValueError: If input contains non-numeric values
    """
    if not input_str.strip():
        return []
    
    try:
        return [int(x.strip()) for x in input_str.split(',')]
    except ValueError as e:
        raise ValueError(f"Invalid input: {e}")


def main():
    """Main function to handle command line input and find single number."""
    if len(sys.argv) != 2:
        print("Usage: python find_single_number.py \"1,2,3,2,1\"", file=sys.stderr)
        sys.exit(1)
    
    # Validate input to prevent command injection
    input_arg = sys.argv[1]
    if not isinstance(input_arg, str):
        print("Error: Invalid input type", file=sys.stderr)
        sys.exit(1)
    
    # Additional validation to ensure input only contains expected characters
    allowed_chars = set('0123456789,- \t')
    if not all(c in allowed_chars for c in input_arg):
        print("Error: Input contains invalid characters. Only numbers, commas, spaces, and minus signs are allowed.", file=sys.stderr)
        sys.exit(1)
    
    try:
        numbers = parse_input(input_arg)
        
        if not numbers:
            print("Error: Input list cannot be empty", file=sys.stderr)
            sys.exit(1)
        
        result = find_single_number(numbers)
        print(result)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
