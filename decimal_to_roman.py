def decimal_to_roman(num):
    """
    Convert a decimal number to Roman numeral.
    
    Args:
        num: Integer between 1 and 3999
        
    Returns:
        str: Roman numeral representation
        
    Raises:
        ValueError: If num is not an integer or not in valid range
    """
    # Check if input is an integer
    if not isinstance(num, int) or isinstance(num, bool):
        raise ValueError(f"Input must be an integer, got {type(num).__name__}")
    
    # Check if number is in valid range
    if num < 1 or num > 3999:
        raise ValueError("Number must be between 1 and 3999")
    
    # Roman numeral mappings in descending order
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
    
    result = ''
    
    for i in range(len(values)):
        count = num // values[i]
        if count:
            result += numerals[i] * count
            num -= values[i] * count
    
    return result


def main():
    """
    Main function to handle command line arguments or interactive input.
    """
    import sys
    
    if len(sys.argv) > 1:
        # Command line argument provided
        try:
            num = int(sys.argv[1])
            roman = decimal_to_roman(num)
            print(f"{num} in Roman numerals is: {roman}")
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                print(f"Error: Invalid input '{sys.argv[1]}' - must be a valid integer")
            else:
                print(f"Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        try:
            num = int(input("Enter a decimal number (1-3999): "))
            roman = decimal_to_roman(num)
            print(f"{num} in Roman numerals is: {roman}")
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")


if __name__ == "__main__":
    main()
