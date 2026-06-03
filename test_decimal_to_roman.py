#!/usr/bin/env python3
"""
Tests for decimal_to_roman module.
"""

import pytest
import sys
from unittest.mock import patch
from decimal_to_roman import decimal_to_roman, main


class TestDecimalToRoman:
    """Test cases for decimal_to_roman function."""
    
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
        """Test conversion of multiples of ten."""
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
        """Test conversion of multiples of one hundred."""
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
        """Test conversion of multiples of one thousand."""
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
    
    def test_boundary_values(self):
        """Test conversion of boundary values."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(3999) == "MMMCMXCIX"
    
    def test_invalid_range_low(self):
        """Test error handling for numbers below valid range."""
        with pytest.raises(ValueError, match="Number must be between 1 and 3999"):
            decimal_to_roman(0)
        with pytest.raises(ValueError, match="Number must be between 1 and 3999"):
            decimal_to_roman(-1)
        with pytest.raises(ValueError, match="Number must be between 1 and 3999"):
            decimal_to_roman(-100)
    
    def test_invalid_range_high(self):
        """Test error handling for numbers above valid range."""
        with pytest.raises(ValueError, match="Number must be between 1 and 3999"):
            decimal_to_roman(4000)
        with pytest.raises(ValueError, match="Number must be between 1 and 3999"):
            decimal_to_roman(5000)
    
    def test_non_integer_types(self):
        """Test error handling for non-integer input types."""
        with pytest.raises(ValueError, match="Input must be an integer"):
            decimal_to_roman("123")
        with pytest.raises(ValueError, match="Input must be an integer"):
            decimal_to_roman(123.0)
        with pytest.raises(ValueError, match="Input must be an integer"):
            decimal_to_roman(123.5)
        with pytest.raises(ValueError, match="Input must be an integer"):
            decimal_to_roman([123])
        with pytest.raises(ValueError, match="Input must be an integer"):
            decimal_to_roman({"num": 123})
        with pytest.raises(ValueError, match="Input must be an integer"):
            decimal_to_roman(None)
        with pytest.raises(ValueError, match="Input must be an integer"):
            decimal_to_roman(True)


class TestMain:
    """Test cases for main function."""
    
    @patch('sys.argv', ['decimal_to_roman.py', '42'])
    @patch('builtins.print')
    def test_main_valid_input(self, mock_print):
        """Test main function with valid input."""
        main()
        mock_print.assert_called_once_with("42 in Roman numerals is: XLII")
    
    @patch('sys.argv', ['decimal_to_roman.py'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_arguments(self, mock_exit, mock_print):
        """Test main function with no arguments."""
        main()
        mock_print.assert_called_once_with("Usage: python decimal_to_roman.py <number>")
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['decimal_to_roman.py', 'abc'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_input(self, mock_exit, mock_print):
        """Test main function with invalid input."""
        main()
        mock_print.assert_called_once_with("Error: Argument must be a valid integer")
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['decimal_to_roman.py', ''])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_empty_argument(self, mock_exit, mock_print):
        """Test main function with empty argument."""
        main()
        mock_print.assert_called_once_with("Error: Empty argument provided")
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['decimal_to_roman.py', '0'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_out_of_range(self, mock_exit, mock_print):
        """Test main function with out of range input."""
        main()
        mock_print.assert_called_once_with("Error: Number must be between 1 and 3999")
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['decimal_to_roman.py', '42'])
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_main_keyboard_interrupt(self, mock_input, mock_exit, mock_print):
        """Test main function with keyboard interrupt."""
        with patch('decimal_to_roman.decimal_to_roman', side_effect=KeyboardInterrupt):
            main()
        mock_print.assert_called_once_with("\nOperation cancelled by user")
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['decimal_to_roman.py', '42'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_unexpected_exception(self, mock_exit, mock_print):
        """Test main function with unexpected exception."""
        with patch('decimal_to_roman.decimal_to_roman', side_effect=RuntimeError("Test error")):
            main()
        mock_print.assert_called_once_with("Unexpected error occurred: RuntimeError: Test error")
        mock_exit.assert_called_once_with(1)
