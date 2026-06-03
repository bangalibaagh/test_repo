#!/usr/bin/env python3
"""Tests for temperature conversion functions."""

import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.temp_convert import celsius_to_fahrenheit, fahrenheit_to_celsius


class TestCelsiusToFahrenheit:
    """Test cases for celsius_to_fahrenheit function."""
    
    def test_freezing_point(self):
        """Test that 0°C equals 32°F."""
        assert celsius_to_fahrenheit(0) == 32.0
    
    def test_boiling_point(self):
        """Test that 100°C equals 212°F."""
        assert celsius_to_fahrenheit(100) == 212.0
    
    def test_negative_forty(self):
        """Test that -40°C equals -40°F."""
        assert celsius_to_fahrenheit(-40) == -40.0
    
    def test_room_temperature(self):
        """Test conversion of room temperature (20°C)."""
        assert celsius_to_fahrenheit(20) == 68.0
    
    def test_float_input(self):
        """Test conversion with float input."""
        result = celsius_to_fahrenheit(25.5)
        expected = 77.9
        assert abs(result - expected) < 0.001


class TestFahrenheitToCelsius:
    """Test cases for fahrenheit_to_celsius function."""
    
    def test_freezing_point(self):
        """Test that 32°F equals 0°C."""
        assert fahrenheit_to_celsius(32) == 0.0
    
    def test_boiling_point(self):
        """Test that 212°F equals 100°C."""
        assert fahrenheit_to_celsius(212) == 100.0
    
    def test_negative_forty(self):
        """Test that -40°F equals -40°C."""
        assert fahrenheit_to_celsius(-40) == -40.0
    
    def test_room_temperature(self):
        """Test conversion of room temperature (68°F)."""
        assert fahrenheit_to_celsius(68) == 20.0
    
    def test_float_input(self):
        """Test conversion with float input."""
        result = fahrenheit_to_celsius(77.9)
        expected = 25.5
        assert abs(result - expected) < 0.001


class TestRoundTrip:
    """Test round-trip conversions to ensure accuracy."""
    
    @pytest.mark.parametrize("celsius_temp", [
        0, 100, -40, 20, 25.5, -273.15, 37.0
    ])
    def test_celsius_round_trip(self, celsius_temp):
        """Test that C -> F -> C returns original value."""
        fahrenheit = celsius_to_fahrenheit(celsius_temp)
        result = fahrenheit_to_celsius(fahrenheit)
        assert abs(result - celsius_temp) < 0.0001
    
    @pytest.mark.parametrize("fahrenheit_temp", [
        32, 212, -40, 68, 77.9, -459.67, 98.6
    ])
    def test_fahrenheit_round_trip(self, fahrenheit_temp):
        """Test that F -> C -> F returns original value."""
        celsius = fahrenheit_to_celsius(fahrenheit_temp)
        result = celsius_to_fahrenheit(celsius)
        assert abs(result - fahrenheit_temp) < 0.0001


class TestEdgeCases:
    """Test edge cases and extreme values."""
    
    def test_absolute_zero_celsius(self):
        """Test absolute zero in Celsius (-273.15°C)."""
        result = celsius_to_fahrenheit(-273.15)
        expected = -459.67
        assert abs(result - expected) < 0.01
    
    def test_absolute_zero_fahrenheit(self):
        """Test absolute zero in Fahrenheit (-459.67°F)."""
        result = fahrenheit_to_celsius(-459.67)
        expected = -273.15
        assert abs(result - expected) < 0.01
