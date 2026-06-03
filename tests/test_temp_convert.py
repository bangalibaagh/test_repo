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
        # Test very large numbers
        large_num = 1e10
        result_c_to_f = celsius_to_fahrenheit(large_num)
        assert math.isfinite(result_c_to_f)
        
        result_f_to_c = fahrenheit_to_celsius(large_num)
        assert math.isfinite(result_f_to_c)
        
        result_c_to_k = celsius_to_kelvin(large_num)
        assert math.isfinite(result_c_to_k)
        
        result_k_to_c = kelvin_to_celsius(large_num)
        assert math.isfinite(result_k_to_c)
        
        # Test very small numbers
        small_num = -1e10
        result_c_to_f = celsius_to_fahrenheit(small_num)
        assert math.isfinite(result_c_to_f)
        
        result_f_to_c = fahrenheit_to_celsius(small_num)
        assert math.isfinite(result_f_to_c)
        
        result_c_to_k = celsius_to_kelvin(small_num)
        assert math.isfinite(result_c_to_k)
        
        result_k_to_c = kelvin_to_celsius(small_num)
        assert math.isfinite(result_k_to_c)
    
    def test_infinity_and_nan(self):
        """Test behavior with infinity and NaN values."""
        # Test positive infinity
        inf_result = celsius_to_fahrenheit(float('inf'))
        assert math.isinf(inf_result)
        
        inf_result = fahrenheit_to_celsius(float('inf'))
        assert math.isinf(inf_result)
        
        inf_result = celsius_to_kelvin(float('inf'))
        assert math.isinf(inf_result)
        
        inf_result = kelvin_to_celsius(float('inf'))
        assert math.isinf(inf_result)
        
        # Test negative infinity
        neg_inf_result = celsius_to_fahrenheit(float('-inf'))
        assert math.isinf(neg_inf_result)
        
        neg_inf_result = fahrenheit_to_celsius(float('-inf'))
        assert math.isinf(neg_inf_result)
        
        neg_inf_result = celsius_to_kelvin(float('-inf'))
        assert math.isinf(neg_inf_result)
        
        neg_inf_result = kelvin_to_celsius(float('-inf'))
        assert math.isinf(neg_inf_result)
        
        # Test NaN
        nan_result = celsius_to_fahrenheit(float('nan'))
        assert math.isnan(nan_result)
        
        nan_result = fahrenheit_to_celsius(float('nan'))
        assert math.isnan(nan_result)
        
        nan_result = celsius_to_kelvin(float('nan'))
        assert math.isnan(nan_result)
        
        nan_result = kelvin_to_celsius(float('nan'))
        assert math.isnan(nan_result)
    
    def test_round_trip_conversions(self):
        """Test that round-trip conversions return to original values."""
        # Celsius -> Fahrenheit -> Celsius
        original = 25.0
        converted = fahrenheit_to_celsius(celsius_to_fahrenheit(original))
        assert abs(converted - original) < self.TOLERANCE
        
        # Fahrenheit -> Celsius -> Fahrenheit
        original = 77.0
        converted = celsius_to_fahrenheit(fahrenheit_to_celsius(original))
        assert abs(converted - original) < self.TOLERANCE
        
        # Celsius -> Kelvin -> Celsius
        original = 25.0
        converted = kelvin_to_celsius(celsius_to_kelvin(original))
        assert abs(converted - original) < self.TOLERANCE
        
        # Kelvin -> Celsius -> Kelvin
        original = 298.15
        converted = celsius_to_kelvin(kelvin_to_celsius(original))
        assert abs(converted - original) < self.TOLERANCE
