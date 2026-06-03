#!/usr/bin/env python3
"""Tests for decimal_to_roman.py"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch

from decimal_to_roman import decimal_to_roman, main


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
        """Test more complex Roman numeral conversions."""
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
    
    def test_large_numbers(self):
        """Test large numbers within valid range."""
        assert decimal_to_roman(1994) == "MCMXCIV"
        assert decimal_to_roman(2023) == "MMXXIII"
        assert decimal_to_roman(3999) == "MMMCMXCIX"
    
    def test_edge_cases(self):
        """Test edge cases at boundaries."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(3999) == "MMMCMXCIX"
    
    def test_invalid_input_zero(self):
        """Test that zero raises ValueError."""
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(0)
    
    def test_invalid_input_negative(self):
        """Test that negative numbers raise ValueError."""
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(-1)
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(-100)
    
    def test_invalid_input_too_large(self):
        """Test that numbers > 3999 raise ValueError."""
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(4000)
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(5000)
    
    def test_invalid_input_non_integer(self):
        """Test that non-integers raise ValueError."""
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(3.14)
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman("42")


class TestMainFunction:
    """Test cases for main function."""
    
    @patch('sys.argv', ['decimal_to_roman.py', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_command_line_valid_input(self, mock_stdout):
        """Test main function with valid command line argument."""
        main()
        assert mock_stdout.getvalue().strip() == "42 in Roman numerals is: XLII"
    
    @patch('sys.argv', ['decimal_to_roman.py', '0'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_command_line_invalid_input(self, mock_stderr):
        """Test main function with invalid command line argument."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        assert "Error: Number must be an integer between 1 and 3999" in mock_stderr.getvalue()
    
    @patch('sys.argv', ['decimal_to_roman.py', 'abc'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_command_line_non_numeric_input(self, mock_stderr):
        """Test main function with non-numeric command line argument."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        assert "Error:" in mock_stderr.getvalue()
    
    @patch('sys.argv', ['decimal_to_roman.py'])
    @patch('builtins.input', return_value='123')
    @patch('sys.stdout', new_callable=StringIO)
    def test_interactive_mode_valid_input(self, mock_stdout, mock_input):
        """Test main function in interactive mode with valid input."""
        main()
        assert mock_stdout.getvalue().strip() == "123 in Roman numerals is: CXXIII"
    
    @patch('sys.argv', ['decimal_to_roman.py'])
    @patch('builtins.input', return_value='0')
    @patch('sys.stderr', new_callable=StringIO)
    def test_interactive_mode_invalid_input(self, mock_stderr, mock_input):
        """Test main function in interactive mode with invalid input."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        assert "Error: Number must be an integer between 1 and 3999" in mock_stderr.getvalue()
    
    @patch('sys.argv', ['decimal_to_roman.py'])
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    @patch('sys.stdout', new_callable=StringIO)
    def test_interactive_mode_keyboard_interrupt(self, mock_stdout, mock_input):
        """Test main function handles KeyboardInterrupt gracefully."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        assert "Goodbye!" in mock_stdout.getvalue()


if __name__ == "__main__":
    pytest.main([__file__])
