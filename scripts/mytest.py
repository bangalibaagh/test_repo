#!/usr/bin/env python3
"""Script that takes 10 numbers as input and sorts them from lowest to highest."""

import sys
from typing import List


def get_numbers() -> List[float]:
    """Get 10 numbers from user input.
    
    Returns:
        List of 10 numbers as floats.
    """
    numbers = []
    print("Please enter 10 numbers:")
    
    for i in range(10):
        while True:
            try:
                num = float(input(f"Enter number {i + 1}: "))
                numbers.append(num)
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    
    return numbers


def sort_numbers(numbers: List[float]) -> List[float]:
    """Sort a list of numbers from lowest to highest.
    
    Args:
        numbers: List of numbers to sort.
        
    Returns:
        Sorted list of numbers.
    """
    return sorted(numbers)


def main() -> None:
    """Main function to run the sorting program."""
    try:
        numbers = get_numbers()
        sorted_numbers = sort_numbers(numbers)
        
        print("\nOriginal numbers:", numbers)
        print("Sorted numbers (lowest to highest):", sorted_numbers)
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
