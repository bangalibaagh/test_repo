#!/usr/bin/env python3
"""Tests for decimal_to_roman.py"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch

from decimal_to_roman import decimal_to_roman, main


class TestDecimalToRoman:
    """Test cases for decimal_to_roman function."""
    
    def test_basic_conversions(self):
        """Test basic Roman numeral conversions."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(2) == "II"
        assert decimal_to_roman(3) == "III"
        assert decimal_to_roman(4) == "IV"
        assert decimal_to_roman(5) == "V"
        assert decimal_to_roman(6) == "VI"
        assert decimal_to_roman(9) == "IX"
        assert decimal_to_roman(10) == "X"
        
    def test_tens_conversions(self):
        """Test conversions for tens."""
        assert decimal_to_roman(20) == "XX"
        assert decimal_to_roman(30) == "XXX"
        assert decimal_to_roman(40) == "XL"
        assert decimal_to_roman(50) == "L"
        assert decimal_to_roman(60) == "LX"
        assert decimal_to_roman(90) == "XC"
        
    def test_hundreds_conversions(self):
        """Test conversions for hundreds."""
        assert decimal_to_roman(100) == "C"
        assert decimal_to_roman(200) == "CC"
        assert decimal_to_roman(300) == "CCC"
        assert decimal_to_roman(400) == "CD"
        assert decimal_to_roman(500) == "D"
        assert decimal_to_roman(600) == "DC"
        assert decimal_to_roman(900) == "CM"
        
    def test_thousands_conversions(self):
        """Test conversions for thousands."""
        assert decimal_to_roman(1000) == "M"
        assert decimal_to_roman(2000) == "MM"
        assert decimal_to_roman(3000) == "MMM"
        
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
        assert decimal_to_roman(3000) == "MMM"
        
    def test_edge_cases(self):
        """Test edge cases."""
        assert decimal_to_roman(1) == "I"  # Minimum value
        assert decimal_to_roman(3999) == "MMMCMXCIX"  # Maximum value
        
    def test_famous_years(self):
        """Test some famous years."""
        assert decimal_to_roman(1984) == "MCMLXXXIV"
        assert decimal_to_roman(2023) == "MMXXIII"
        assert decimal_to_roman(1776) == "MDCCLXXVI"
        assert decimal_to_roman(2000) == "MM"
        
    def test_invalid_inputs(self):
        """Test invalid input handling."""
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(0)
            
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(-1)
            
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(4000)
            
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(10000)
            
    def test_non_integer_inputs(self):
        """Test non-integer input handling."""
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(3.14)
            
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman("42")
            
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(None)


class TestMainFunction:
    """Test cases for main function."""
    
    @patch('sys.argv', ['decimal_to_roman.py', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_command_line_argument_valid(self, mock_stdout):
        """Test main function with valid command line argument."""
        main()
        assert "42 in Roman numerals is: XLII" in mock_stdout.getvalue()
        
    @patch('sys.argv', ['decimal_to_roman.py', '0'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_command_line_argument_invalid(self, mock_stderr):
        """Test main function with invalid command line argument."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        assert "Error: Number must be an integer between 1 and 3999" in mock_stderr.getvalue()
        
    @patch('sys.argv', ['decimal_to_roman.py', 'abc'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_command_line_argument_non_numeric(self, mock_stderr):
        """Test main function with non-numeric command line argument."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        assert "Error:" in mock_stderr.getvalue()
        
    @patch('sys.argv', ['decimal_to_roman.py'])
    @patch('builtins.input', return_value='123')
    @patch('sys.stdout', new_callable=StringIO)
    def test_interactive_mode_valid(self, mock_stdout, mock_input):
        """Test main function in interactive mode with valid input."""
        main()
        assert "123 in Roman numerals is: CXXIII" in mock_stdout.getvalue()
        
    @patch('sys.argv', ['decimal_to_roman.py'])
    @patch('builtins.input', return_value='0')
    @patch('sys.stderr', new_callable=StringIO)
    def test_interactive_mode_invalid(self, mock_stderr, mock_input):
        """Test main function in interactive mode with invalid input."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        assert "Error: Number must be an integer between 1 and 3999" in mock_stderr.getvalue()
        
    @patch('sys.argv', ['decimal_to_roman.py'])
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    @patch('sys.stdout', new_callable=StringIO)
    def test_interactive_mode_keyboard_interrupt(self, mock_stdout, mock_input):
        """Test main function handling KeyboardInterrupt in interactive mode."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        assert "Goodbye!" in mock_stdout.getvalue()


if __name__ == "__main__":
    pytest.main([__file__])
