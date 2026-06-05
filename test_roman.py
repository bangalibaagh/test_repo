#!/usr/bin/env python3
"""Tests for roman.py module."""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

from roman import decimal_to_roman, get_user_input, main


class TestDecimalToRoman:
    """Test cases for decimal_to_roman function."""
    
    def test_basic_numbers(self):
        """Test basic Roman numeral conversions."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(2) == "II"
        assert decimal_to_roman(3) == "III"
        assert decimal_to_roman(4) == "IV"
        assert decimal_to_roman(5) == "V"
        assert decimal_to_roman(6) == "VI"
        assert decimal_to_roman(9) == "IX"
        assert decimal_to_roman(10) == "X"
    
    def test_tens_and_hundreds(self):
        """Test tens and hundreds conversions."""
        assert decimal_to_roman(20) == "XX"
        assert decimal_to_roman(30) == "XXX"
        assert decimal_to_roman(40) == "XL"
        assert decimal_to_roman(50) == "L"
        assert decimal_to_roman(90) == "XC"
        assert decimal_to_roman(100) == "C"
        assert decimal_to_roman(400) == "CD"
        assert decimal_to_roman(500) == "D"
        assert decimal_to_roman(900) == "CM"
        assert decimal_to_roman(1000) == "M"
    
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
    
    def test_edge_cases(self):
        """Test edge cases for Roman numeral conversion."""
        assert decimal_to_roman(1) == "I"  # Minimum
        assert decimal_to_roman(3999) == "MMMCMXCIX"  # Maximum
        assert decimal_to_roman(1994) == "MCMXCIV"
        assert decimal_to_roman(2023) == "MMXXIII"
    
    def test_invalid_inputs(self):
        """Test invalid inputs raise ValueError."""
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(0)
        
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(-1)
        
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(4000)
        
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(10000)
    
    def test_non_integer_inputs(self):
        """Test non-integer inputs raise ValueError."""
        with pytest.raises(ValueError):
            decimal_to_roman(3.14)
        
        with pytest.raises(ValueError):
            decimal_to_roman("42")


class TestGetUserInput:
    """Test cases for get_user_input function."""
    
    @patch('builtins.input', return_value='42')
    def test_valid_input(self, mock_input):
        """Test valid integer input."""
        result = get_user_input()
        assert result == 42
    
    @patch('builtins.input', return_value='not_a_number')
    def test_invalid_input(self, mock_input):
        """Test invalid input returns None."""
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input', side_effect=EOFError)
    def test_eof_input(self, mock_input):
        """Test EOF input returns None."""
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_input):
        """Test KeyboardInterrupt is propagated."""
        with pytest.raises(KeyboardInterrupt):
            get_user_input()


class TestMain:
    """Test cases for main function."""
    
    @patch('sys.argv', ['roman.py', '42'])
    @patch('builtins.print')
    def test_command_line_valid_number(self, mock_print):
        """Test command line with valid number."""
        main()
        mock_print.assert_called_once_with("42 = XLII")
    
    @patch('sys.argv', ['roman.py', '0'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_command_line_invalid_number(self, mock_exit, mock_print):
        """Test command line with invalid number."""
        main()
        mock_print.assert_called_once()
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['roman.py', 'not_a_number'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_command_line_non_numeric(self, mock_exit, mock_print):
        """Test command line with non-numeric argument."""
        main()
        mock_print.assert_called_once()
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['roman.py', '1', '2', '3'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_command_line_too_many_args(self, mock_exit, mock_print):
        """Test command line with too many arguments."""
        main()
        mock_print.assert_called_once_with("Usage: python roman.py [number]", file=sys.stderr)
        mock_exit.assert_called_once_with(1)
