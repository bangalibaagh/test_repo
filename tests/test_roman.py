#!/usr/bin/env python3
"""Tests for Roman numeral conversion script."""

import pytest
from scripts.roman import decimal_to_roman


class TestDecimalToRoman:
    """Test cases for decimal to Roman numeral conversion."""
    
    def test_basic_numbers(self):
        """Test basic single digit conversions."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(2) == "II"
        assert decimal_to_roman(3) == "III"
        assert decimal_to_roman(5) == "V"
        assert decimal_to_roman(10) == "X"
    
    def test_subtractive_cases(self):
        """Test subtractive notation cases."""
        assert decimal_to_roman(4) == "IV"
        assert decimal_to_roman(9) == "IX"
        assert decimal_to_roman(40) == "XL"
        assert decimal_to_roman(90) == "XC"
        assert decimal_to_roman(400) == "CD"
        assert decimal_to_roman(900) == "CM"
    
    def test_composite_numbers(self):
        """Test composite numbers with multiple Roman numeral components."""
        assert decimal_to_roman(27) == "XXVII"  # 10 + 10 + 5 + 1 + 1
        assert decimal_to_roman(48) == "XLVIII"  # 40 + 5 + 1 + 1 + 1
        assert decimal_to_roman(59) == "LIX"  # 50 + 9
        assert decimal_to_roman(93) == "XCIII"  # 90 + 3
        assert decimal_to_roman(141) == "CXLI"  # 100 + 40 + 1
        assert decimal_to_roman(163) == "CLXIII"  # 100 + 50 + 10 + 3
        assert decimal_to_roman(402) == "CDII"  # 400 + 2
        assert decimal_to_roman(575) == "DLXXV"  # 500 + 50 + 20 + 5
        assert decimal_to_roman(911) == "CMXI"  # 900 + 10 + 1
        assert decimal_to_roman(1024) == "MXXIV"  # 1000 + 20 + 4
    
    def test_large_numbers(self):
        """Test larger numbers."""
        assert decimal_to_roman(1000) == "M"
        assert decimal_to_roman(1994) == "MCMXCIV"  # 1000 + 900 + 90 + 4
        assert decimal_to_roman(2023) == "MMXXIII"  # 2000 + 20 + 3
        assert decimal_to_roman(3999) == "MMMCMXCIX"  # 3000 + 900 + 90 + 9
    
    def test_edge_cases(self):
        """Test edge cases and boundary values."""
        # Minimum value
        assert decimal_to_roman(1) == "I"
        # Maximum value
        assert decimal_to_roman(3999) == "MMMCMXCIX"
    
    def test_invalid_inputs(self):
        """Test invalid input handling."""
        # Test zero
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(0)
        
        # Test negative numbers
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(-1)
        
        # Test numbers too large
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(4000)
        
        # Test non-integer types
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(3.14)
        
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman("42")
    
    def test_specific_requested_cases(self):
        """Test the specific cases mentioned in the task."""
        # Single cases
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(4) == "IV"
        assert decimal_to_roman(9) == "IX"
        assert decimal_to_roman(40) == "XL"
        assert decimal_to_roman(90) == "XC"
        assert decimal_to_roman(400) == "CD"
        assert decimal_to_roman(900) == "CM"
        
        # Additional composite numbers
        assert decimal_to_roman(44) == "XLIV"  # 40 + 4
        assert decimal_to_roman(49) == "XLIX"  # 40 + 9
        assert decimal_to_roman(94) == "XCIV"  # 90 + 4
        assert decimal_to_roman(99) == "XCIX"  # 90 + 9
        assert decimal_to_roman(444) == "CDXLIV"  # 400 + 40 + 4
        assert decimal_to_roman(949) == "CMXLIX"  # 900 + 40 + 9
