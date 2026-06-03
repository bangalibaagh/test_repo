#!/usr/bin/env python3
"""
Script to find the single number in a comma-separated list where all other numbers appear exactly twice.

Usage:
    python find_single_number.py "1,2,1,3,2"
    echo "1,2,1,3,2" | python find_single_number.py
"""

import sys
from typing import List


def find_single_number(numbers: List[int]) -> int:
    """
    Find the number that appears exactly once in a list where all other numbers appear twice.
    
    Uses XOR operation which has the property that:
    - a ^ a = 0 (any number XORed with itself is 0)
    - a ^ 0 = a (any number XORed with 0 is itself)
    - XOR is commutative and associative
    
    Args:
        numbers: List of integers where all numbers appear twice except one
        
    Returns:
        The number that appears exactly once
    """
    result = 0
    for num in numbers:
        result ^= num
    return result


def parse_input(input_str: str) -> List[int]:
    """
    Parse comma-separated string of numbers into a list of integers.
    
    Args:
        input_str: Comma-separated string of numbers
        
    Returns:
        List of integers
        
    Raises:
        ValueError: If input contains non-numeric values
    """
    try:
        return [int(x.strip()) for x in input_str.split(',')]
    except ValueError as e:
        raise ValueError(f"Invalid input: all values must be numbers. Error: {e}")


def main():
    """
    Main function to handle command line input and find the single number.
    """
    try:
        # Check if input is provided as command line argument
        if len(sys.argv) > 1:
            input_str = sys.argv[1]
        else:
            # Read from stdin
            try:
                input_str = input().strip()
            except EOFError:
                print("Error: No input provided", file=sys.stderr)
                sys.exit(1)
        
        if not input_str:
            print("Error: No input provided", file=sys.stderr)
            sys.exit(1)
        
        numbers = parse_input(input_str)
        
        if len(numbers) == 0:
            print("Error: Empty input", file=sys.stderr)
            sys.exit(1)
        
        single_number = find_single_number(numbers)
        print(single_number)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
