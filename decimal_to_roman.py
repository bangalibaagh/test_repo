def decimal_to_roman(num):
    """
    Convert a decimal number to Roman numeral.
    
    Args:
        num: Integer between 1 and 3999 (inclusive)
        
    Returns:
        str: Roman numeral representation
        
    Raises:
        ValueError: If num is not an integer or is outside valid range
        TypeError: If num is not a number type
    """
    # Type validation
    if not isinstance(num, int):
        raise TypeError(f"Input must be an integer, got {type(num).__name__}")
    
    # Range validation
    if num < 1 or num > 3999:
        raise ValueError(f"Number must be between 1 and 3999, got {num}")
    
    # Roman numeral mapping in descending order
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
    
    result = ''
    
    for i in range(len(values)):
        count = num // values[i]
        if count:
            result += symbols[i] * count
            num -= values[i] * count
    
    return result


def main():
    """
    Main function to handle command line arguments or interactive input.
    """
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        try:
            num = int(sys.argv[1])
        except ValueError:
            print(f"Error: '{sys.argv[1]}' is not a valid integer")
            return
        
        try:
            roman = decimal_to_roman(num)
            print(f"{num} in Roman numerals is: {roman}")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
    else:
        # Interactive mode
        try:
            user_input = input("Enter a decimal number (1-3999): ")
            try:
                num = int(user_input)
            except ValueError:
                print(f"Error: '{user_input}' is not a valid integer")
                return
            
            roman = decimal_to_roman(num)
            print(f"{num} in Roman numerals is: {roman}")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")


if __name__ == "__main__":
    main()
