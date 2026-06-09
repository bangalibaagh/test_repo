#!/usr/bin/env python3
"""Tests for Roman numeral converter.

Follows STD-003 testing standards with comprehensive test coverage.
"""

import pytest
import sys
from unittest.mock import patch
from io import StringIO

# Add scripts directory to path for importing
sys.path.insert(0, 'scripts')
from roman import decimal_to_roman, main


class TestDecimalToRoman:
    """Test cases for decimal_to_roman function."""
    
    def test_basic_numerals(self):
        """Test basic Roman numeral conversions."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(5) == "V"
        assert decimal_to_roman(10) == "X"
        assert decimal_to_roman(50) == "L"
        assert decimal_to_roman(100) == "C"
        assert decimal_to_roman(500) == "D"
        assert decimal_to_roman(1000) == "M"
    
    def test_subtractive_notation(self):
        """Test subtractive notation cases."""
        assert decimal_to_roman(4) == "IV"
        assert decimal_to_roman(9) == "IX"
        assert decimal_to_roman(40) == "XL"
        assert decimal_to_roman(90) == "XC"
        assert decimal_to_roman(400) == "CD"
        assert decimal_to_roman(900) == "CM"
    
    def test_complex_numbers(self):
        """Test complex Roman numeral conversions."""
        assert decimal_to_roman(27) == "XXVII"
        assert decimal_to_roman(48) == "XLVIII"
        assert decimal_to_roman(59) == "LIX"
        assert decimal_to_roman(93) == "XCIII"
        assert decimal_to_roman(141) == "CXLI"
        assert decimal_to_roman(163) == "CLXIII"
        assert decimal_to_roman(402) == "CDII"
        assert decimal_to_roman(575) == "DLXXV"
        assert decimal_to_roman(911) == "CMXI"
        assert decimal_to_roman(1024) == "MXXIV"
    
    def test_boundary_values(self):
        """Test boundary values."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(3999) == "MMMCMXCIX"
    
    def test_numbers_and_special_chars(self):
        """Test edge cases with invalid inputs - following existing test pattern."""
        # Test invalid range - too small
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(0)
        
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(-1)
        
        # Test invalid range - too large
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(4000)
        
        # Test invalid type
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman("42")
        
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(3.14)
    
    def test_large_numbers(self):
        """Test larger valid numbers."""
        assert decimal_to_roman(1994) == "MCMXCIV"
        assert decimal_to_roman(2023) == "MMXXIII"
        assert decimal_to_roman(3888) == "MMMDCCCLXXXVIII"


class TestMainFunction:
    """Test cases for main function and CLI interface."""
    
    def test_valid_input(self, capsys):
        """Test main function with valid input."""
        with patch('sys.argv', ['roman.py', '42']):
            main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "XLII"
        assert captured.err == ""
    
    def test_no_arguments(self, capsys):
        """Test main function with no arguments."""
        with patch('sys.argv', ['roman.py']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Usage: python roman.py <decimal_number>" in captured.err
    
    def test_too_many_arguments(self, capsys):
        """Test main function with too many arguments."""
        with patch('sys.argv', ['roman.py', '42', '24']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Usage: python roman.py <decimal_number>" in captured.err
    
    def test_invalid_number_input(self, capsys):
        """Test main function with invalid number input."""
        with patch('sys.argv', ['roman.py', 'abc']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Error:" in captured.err
    
    def test_out_of_range_input(self, capsys):
        """Test main function with out of range input."""
        with patch('sys.argv', ['roman.py', '0']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Error: Number must be an integer between 1 and 3999" in captured.err
    
    def test_boundary_inputs_cli(self, capsys):
        """Test CLI with boundary inputs."""
        # Test minimum valid input
        with patch('sys.argv', ['roman.py', '1']):
            main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "I"
        
        # Test maximum valid input
        with patch('sys.argv', ['roman.py', '3999']):
            main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "MMMCMXCIX"
