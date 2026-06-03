#!/usr/bin/env python3
"""
Test suite for decimal_to_roman.py

Tests the decimal to Roman numeral conversion functionality.
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch

from decimal_to_roman import decimal_to_roman, main


class TestDecimalToRoman:
    """Test cases for the decimal_to_roman function."""
    
    def test_single_digits(self):
        """Test conversion of single digit numbers."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(2) == "II"
        assert decimal_to_roman(3) == "III"
        assert decimal_to_roman(4) == "IV"
        assert decimal_to_roman(5) == "V"
        assert decimal_to_roman(6) == "VI"
        assert decimal_to_roman(7) == "VII"
        assert decimal_to_roman(8) == "VIII"
        assert decimal_to_roman(9) == "IX"
    
    def test_tens(self):
        """Test conversion of numbers involving tens."""
        assert decimal_to_roman(10) == "X"
        assert decimal_to_roman(20) == "XX"
        assert decimal_to_roman(30) == "XXX"
        assert decimal_to_roman(40) == "XL"
        assert decimal_to_roman(50) == "L"
        assert decimal_to_roman(60) == "LX"
        assert decimal_to_roman(70) == "LXX"
        assert decimal_to_roman(80) == "LXXX"
        assert decimal_to_roman(90) == "XC"
    
    def test_hundreds(self):
        """Test conversion of numbers involving hundreds."""
        assert decimal_to_roman(100) == "C"
        assert decimal_to_roman(200) == "CC"
        assert decimal_to_roman(300) == "CCC"
        assert decimal_to_roman(400) == "CD"
        assert decimal_to_roman(500) == "D"
        assert decimal_to_roman(600) == "DC"
        assert decimal_to_roman(700) == "DCC"
        assert decimal_to_roman(800) == "DCCC"
        assert decimal_to_roman(900) == "CM"
    
    def test_thousands(self):
        """Test conversion of numbers involving thousands."""
        assert decimal_to_roman(1000) == "M"
        assert decimal_to_roman(2000) == "MM"
        assert decimal_to_roman(3000) == "MMM"
    
    def test_complex_numbers(self):
        """Test conversion of complex multi-digit numbers."""
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
        assert decimal_to_roman(3000) == "MMM"
    
    def test_edge_cases(self):
        """Test edge cases at boundaries."""
        assert decimal_to_roman(1) == "I"  # Minimum value
        assert decimal_to_roman(3999) == "MMMCMXCIX"  # Maximum value
    
    def test_famous_years(self):
        """Test conversion of some famous years."""
        assert decimal_to_roman(1776) == "MDCCLXXVI"  # American Independence
        assert decimal_to_roman(1969) == "MCMLXIX"    # Moon landing
        assert decimal_to_roman(2000) == "MM"          # Y2K
        assert decimal_to_roman(2023) == "MMXXIII"     # Recent year
    
    def test_invalid_inputs(self):
        """Test that invalid inputs raise appropriate errors."""
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(0)
        
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(-1)
        
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(4000)
        
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(10000)
    
    def test_non_integer_inputs(self):
        """Test that non-integer inputs raise appropriate errors."""
        with pytest.raises(ValueError):
            decimal_to_roman(3.14)
        
        with pytest.raises(ValueError):
            decimal_to_roman("42")
        
        with pytest.raises(ValueError):
            decimal_to_roman(None)


class TestMainFunction:
    """Test cases for the main function."""
    
    @patch('builtins.input', return_value='42')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_valid_input(self, mock_stdout, mock_input):
        """Test main function with valid user input."""
        result = main()
        assert result == 0
        assert "42 in Roman numerals is: XLII" in mock_stdout.getvalue()
    
    @patch('builtins.input', return_value='abc')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_invalid_input(self, mock_stdout, mock_input):
        """Test main function with invalid user input."""
        result = main()
        assert result == 1
        assert "Error: Please enter a valid integer." in mock_stdout.getvalue()
    
    @patch('builtins.input', return_value='0')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_out_of_range_input(self, mock_stdout, mock_input):
        """Test main function with out of range input."""
        result = main()
        assert result == 1
        assert "Error: Number must be an integer between 1 and 3999" in mock_stdout.getvalue()
    
    @patch('sys.argv', ['decimal_to_roman.py', '123'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_command_line_argument(self, mock_stdout):
        """Test main function with command line argument."""
        result = main()
        assert result == 0
        assert "123 in Roman numerals is: CXXIII" in mock_stdout.getvalue()
    
    @patch('sys.argv', ['decimal_to_roman.py', 'invalid'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_invalid_command_line_argument(self, mock_stdout):
        """Test main function with invalid command line argument."""
        result = main()
        assert result == 1
        assert "Error: Please enter a valid integer." in mock_stdout.getvalue()
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_keyboard_interrupt(self, mock_stdout, mock_input):
        """Test main function handles keyboard interrupt gracefully."""
        result = main()
        assert result == 1
        assert "Operation cancelled." in mock_stdout.getvalue()


if __name__ == "__main__":
    pytest.main([__file__])
