#!/usr/bin/env python3
"""Simple calculator script that takes two input numbers and prints their sum."""

import sys
from typing import Union


def get_number_input(prompt: str, max_attempts: int = 3) -> float:
    """Get a number input from the user with validation.
    
    Args:
        prompt: The prompt message to display to the user
        max_attempts: Maximum number of attempts before raising an exception
        
    Returns:
        The validated number as a float
        
    Raises:
        ValueError: If the input is not a valid number after max_attempts
    """
    attempts = 0
    while attempts < max_attempts:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                raise ValueError("Input cannot be empty")
            return float(user_input)
        except ValueError as e:
            attempts += 1
            if "could not convert" in str(e):
                print("Error: Please enter a valid number.")
            else:
                print(f"Error: {e}")
            
            if attempts >= max_attempts:
                raise ValueError(f"Failed to get valid input after {max_attempts} attempts")
    
    # This should never be reached due to the raise above, but included for completeness
    raise ValueError(f"Failed to get valid input after {max_attempts} attempts")


def add_numbers(num1: Union[int, float], num2: Union[int, float]) -> Union[int, float]:
    """Add two numbers together.
    
    Args:
        num1: First number
        num2: Second number
        
    Returns:
        The sum of the two numbers
    """
    return num1 + num2


def main() -> None:
    """Main function to run the calculator."""
    try:
        print("Simple Calculator - Addition")
        print("=============================")
        
        # Get two numbers from user input
        first_number = get_number_input("Enter the first number: ")
        second_number = get_number_input("Enter the second number: ")
        
        # Calculate and display the sum
        result = add_numbers(first_number, second_number)
        
        # Format output to avoid unnecessary decimal places for whole numbers
        if result == int(result):
            print(f"\nResult: {int(result)}")
        else:
            print(f"\nResult: {result}")
            
    except KeyboardInterrupt:
        print("\n\nCalculation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
