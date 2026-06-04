#!/usr/bin/env python3
"""Temperature conversion utilities."""


def celsius_to_fahrenheit(c: float) -> float:
    """Convert temperature from Celsius to Fahrenheit.
    
    Args:
        c: Temperature in Celsius
        
    Returns:
        Temperature in Fahrenheit
        
    Examples:
        >>> celsius_to_fahrenheit(0)
        32.0
        >>> celsius_to_fahrenheit(100)
        212.0
        >>> celsius_to_fahrenheit(-40)
        -40.0
    """
    return (c * 9/5) + 32


if __name__ == "__main__":
    # Example usage
    test_temps = [0, 25, 100, -40, -273.15]
    for temp_c in test_temps:
        temp_f = celsius_to_fahrenheit(temp_c)
        print(f"{temp_c}°C = {temp_f}°F")
