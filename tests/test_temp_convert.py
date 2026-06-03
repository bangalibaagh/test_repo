#!/usr/bin/env python3
"""Tests for temperature conversion functions."""

import math
import pytest
from temp_convert import celsius_to_fahrenheit, fahrenheit_to_celsius, celsius_to_kelvin, kelvin_to_celsius


class TestTemperatureConversions:
    """Test class for all temperature conversion functions."""
    
    # Standard tolerance for floating point comparisons
    TOLERANCE = 0.001
    
    def test_celsius_to_fahrenheit_basic(self):
        """Test basic Celsius to Fahrenheit conversions."""
        assert abs(celsius_to_fahrenheit(0) - 32.0) < self.TOLERANCE
        assert abs(celsius_to_fahrenheit(100) - 212.0) < self.TOLERANCE
        assert abs(celsius_to_fahrenheit(-40) - (-40.0)) < self.TOLERANCE
        assert abs(celsius_to_fahrenheit(37) - 98.6) < self.TOLERANCE
    
    def test_fahrenheit_to_celsius_basic(self):
        """Test basic Fahrenheit to Celsius conversions."""
        assert abs(fahrenheit_to_celsius(32) - 0.0) < self.TOLERANCE
        assert abs(fahrenheit_to_celsius(212) - 100.0) < self.TOLERANCE
        assert abs(fahrenheit_to_celsius(-40) - (-40.0)) < self.TOLERANCE
        assert abs(fahrenheit_to_celsius(98.6) - 37.0) < self.TOLERANCE
    
    def test_celsius_to_kelvin_basic(self):
        """Test basic Celsius to Kelvin conversions."""
        assert abs(celsius_to_kelvin(0) - 273.15) < self.TOLERANCE
        assert abs(celsius_to_kelvin(100) - 373.15) < self.TOLERANCE
        assert abs(celsius_to_kelvin(-273.15) - 0.0) < self.TOLERANCE
    
    def test_kelvin_to_celsius_basic(self):
        """Test basic Kelvin to Celsius conversions."""
        assert abs(kelvin_to_celsius(273.15) - 0.0) < self.TOLERANCE
        assert abs(kelvin_to_celsius(373.15) - 100.0) < self.TOLERANCE
        assert abs(kelvin_to_celsius(0) - (-273.15)) < self.TOLERANCE
    
    def test_negative_temperatures(self):
        """Test conversions with negative temperatures."""
        assert abs(celsius_to_fahrenheit(-10) - 14.0) < self.TOLERANCE
        assert abs(fahrenheit_to_celsius(14) - (-10.0)) < self.TOLERANCE
        assert abs(celsius_to_kelvin(-10) - 263.15) < self.TOLERANCE
        assert abs(kelvin_to_celsius(263.15) - (-10.0)) < self.TOLERANCE
    
    def test_fractional_temperatures(self):
        """Test conversions with fractional temperatures."""
        assert abs(celsius_to_fahrenheit(25.5) - 77.9) < self.TOLERANCE
        assert abs(fahrenheit_to_celsius(77.9) - 25.5) < self.TOLERANCE
        assert abs(celsius_to_kelvin(25.5) - 298.65) < self.TOLERANCE
        assert abs(kelvin_to_celsius(298.65) - 25.5) < self.TOLERANCE
    
    def test_invalid_input_types(self):
        """Test that functions handle invalid input types appropriately."""
        # Test string inputs
        with pytest.raises(TypeError):
            celsius_to_fahrenheit("not a number")
        with pytest.raises(TypeError):
            fahrenheit_to_celsius("not a number")
        with pytest.raises(TypeError):
            celsius_to_kelvin("not a number")
        with pytest.raises(TypeError):
            kelvin_to_celsius("not a number")
        
        # Test None inputs
        with pytest.raises(TypeError):
            celsius_to_fahrenheit(None)
        with pytest.raises(TypeError):
            fahrenheit_to_celsius(None)
        with pytest.raises(TypeError):
            celsius_to_kelvin(None)
        with pytest.raises(TypeError):
            kelvin_to_celsius(None)
        
        # Test object inputs
        with pytest.raises(TypeError):
            celsius_to_fahrenheit({})
        with pytest.raises(TypeError):
            fahrenheit_to_celsius([])
        with pytest.raises(TypeError):
            celsius_to_kelvin(object())
        with pytest.raises(TypeError):
            kelvin_to_celsius(set())
    
    def test_extreme_numeric_values(self):
        """Test conversions with extreme numeric values."""
        # Test infinity
        assert celsius_to_fahrenheit(float('inf')) == float('inf')
        assert fahrenheit_to_celsius(float('inf')) == float('inf')
        assert celsius_to_kelvin(float('inf')) == float('inf')
        assert kelvin_to_celsius(float('inf')) == float('inf')
        
        assert celsius_to_fahrenheit(float('-inf')) == float('-inf')
        assert fahrenheit_to_celsius(float('-inf')) == float('-inf')
        assert celsius_to_kelvin(float('-inf')) == float('-inf')
        assert kelvin_to_celsius(float('-inf')) == float('-inf')
        
        # Test NaN
        assert math.isnan(celsius_to_fahrenheit(float('nan')))
        assert math.isnan(fahrenheit_to_celsius(float('nan')))
        assert math.isnan(celsius_to_kelvin(float('nan')))
        assert math.isnan(kelvin_to_celsius(float('nan')))
        
        # Test very large numbers
        large_num = 1e100
        result_c_to_f = celsius_to_fahrenheit(large_num)
        assert result_c_to_f > large_num  # Should be larger due to conversion
        
        result_f_to_c = fahrenheit_to_celsius(large_num)
        assert abs(result_f_to_c - (large_num - 32) * 5/9) < large_num * 1e-10
        
        result_c_to_k = celsius_to_kelvin(large_num)
        assert abs(result_c_to_k - (large_num + 273.15)) < large_num * 1e-10
        
        result_k_to_c = kelvin_to_celsius(large_num)
        assert abs(result_k_to_c - (large_num - 273.15)) < large_num * 1e-10
