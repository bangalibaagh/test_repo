#!/usr/bin/env python3
"""Temperature conversion utilities.

This module provides functions to convert between Celsius and Fahrenheit temperature scales.
"""

from typing import Union


def celsius_to_fahrenheit(celsius: Union[int, float]) -> float:
    """Convert temperature from Celsius to Fahrenheit.
    
    Args:
        celsius: Temperature in degrees Celsius
        
    Returns:
        Temperature in degrees Fahrenheit
        
    Examples:
        >>> celsius_to_fahrenheit(0)
        32.0
        >>> celsius_to_fahrenheit(100)
        212.0
        >>> celsius_to_fahrenheit(-40)
        -40.0
    """
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit: Union[int, float]) -> float:
    """Convert temperature from Fahrenheit to Celsius.
    
    Args:
        fahrenheit: Temperature in degrees Fahrenheit
        
    Returns:
        Temperature in degrees Celsius
        
    Examples:
        >>> fahrenheit_to_celsius(32)
        0.0
        >>> fahrenheit_to_celsius(212)
        100.0
        >>> fahrenheit_to_celsius(-40)
        -40.0
    """
    return (fahrenheit - 32) * 5/9
