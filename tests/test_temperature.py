#!/usr/bin/env python3
"""Tests for temperature conversion functions."""

import pytest
import sys
import os

# Add scripts directory to path so we can import temperature module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from temperature import celsius_to_fahrenheit


class TestCelsiusToFahrenheit:
    """Test cases for celsius_to_fahrenheit function."""
    
    def test_normal_positive_temperature(self):
        """Test conversion of normal positive temperatures."""
        # Room temperature
        assert celsius_to_fahrenheit(25) == 77.0
        
        # Body temperature
        assert celsius_to_fahrenheit(37) == 98.6
        
        # Boiling point of water
        assert celsius_to_fahrenheit(100) == 212.0
        
    def test_zero_temperature(self):
        """Test conversion of zero degrees Celsius."""
        # Freezing point of water
        assert celsius_to_fahrenheit(0) == 32.0
        
    def test_negative_temperatures(self):
        """Test conversion of negative temperatures."""
        # Below freezing
        assert celsius_to_fahrenheit(-10) == 14.0
        
        # Very cold temperature
        assert celsius_to_fahrenheit(-40) == -40.0
        
        # Absolute zero (theoretical)
        result = celsius_to_fahrenheit(-273.15)
        assert abs(result - (-459.67)) < 0.01  # Using approximate comparison for floating point
        
    def test_decimal_temperatures(self):
        """Test conversion with decimal inputs."""
        assert celsius_to_fahrenheit(36.5) == 97.7
        # Use approximate comparison for floating point precision issues
        result = celsius_to_fahrenheit(-17.8)
        assert abs(result - 0.0) < 0.1
        
    def test_extreme_temperatures(self):
        """Test conversion of extreme temperature values."""
        # Very hot
        assert celsius_to_fahrenheit(1000) == 1832.0
        
        # Very cold
        assert celsius_to_fahrenheit(-200) == -328.0