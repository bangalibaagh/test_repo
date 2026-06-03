def decimal_to_roman(num):
    """
    Convert a decimal number to Roman numeral.
    
    Args:
        num (int): A positive integer between 1 and 3999
        
    Returns:
        str: Roman numeral representation
        
    Raises:
        ValueError: If num is not an integer or is out of valid range
    """
    # Input validation
    if not isinstance(num, int):
        raise ValueError("Input must be an integer")
    
    if num <= 0 or num > 3999:
        raise ValueError("Number must be between 1 and 3999")
    
    # Roman numeral mappings in descending order
    values = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    
    numerals = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    
    result = ""
    
    # Convert to Roman numerals
    for i in range(len(values)):
        count = num // values[i]
        if count:
            result += numerals[i] * count
            num -= values[i] * count
    
    return result


def main():
    """
    Main function to demonstrate decimal to Roman numeral conversion.
    """
    try:
        # Get input from user
        user_input = input("Enter a decimal number (1-3999): ")
        
        # Convert to integer
        decimal_num = int(user_input)
        
        # Convert to Roman numeral
        roman_numeral = decimal_to_roman(decimal_num)
        
        print(f"{decimal_num} in Roman numerals is: {roman_numeral}")
        
    except ValueError as e:
        if "invalid literal" in str(e):
            print("Error: Please enter a valid integer")
        else:
            print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
