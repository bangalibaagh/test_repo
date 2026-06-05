#!/usr/bin/env python3
"""Tests for roman.py module."""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

from roman import decimal_to_roman, get_user_input, main


class TestDecimalToRoman:
    """Test cases for decimal_to_roman function."""
    
    def test_basic_conversions(self):
        """Test basic Roman numeral conversions."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(2) == "II"
        assert decimal_to_roman(3) == "III"
        assert decimal_to_roman(4) == "IV"
        assert decimal_to_roman(5) == "V"
        assert decimal_to_roman(9) == "IX"
        assert decimal_to_roman(10) == "X"
        assert decimal_to_roman(40) == "XL"
        assert decimal_to_roman(50) == "L"
        assert decimal_to_roman(90) == "XC"
        assert decimal_to_roman(100) == "C"
        assert decimal_to_roman(400) == "CD"
        assert decimal_to_roman(500) == "D"
        assert decimal_to_roman(900) == "CM"
        assert decimal_to_roman(1000) == "M"
    
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
    
    def test_edge_cases(self):
        """Test edge cases for Roman numeral conversion."""
        assert decimal_to_roman(1) == "I"  # Minimum value
        assert decimal_to_roman(3999) == "MMMCMXCIX"  # Maximum value
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
        
        with pytest.raises(ValueError):
            decimal_to_roman(None)


class TestGetUserInput:
    """Test cases for get_user_input function."""
    
    @patch('builtins.input')
    def test_valid_input(self, mock_input):
        """Test valid user input."""
        mock_input.return_value = "42"
        result = get_user_input()
        assert result == 42
    
    @patch('builtins.input')
    def test_invalid_input(self, mock_input):
        """Test invalid user input returns None."""
        mock_input.return_value = "not_a_number"
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input')
    def test_empty_input(self, mock_input):
        """Test empty input returns None."""
        mock_input.return_value = ""
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input')
    def test_whitespace_input(self, mock_input):
        """Test whitespace-only input returns None."""
        mock_input.return_value = "   "
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input')
    def test_eof_error(self, mock_input):
        """Test EOFError returns None."""
        mock_input.side_effect = EOFError()
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input')
    def test_keyboard_interrupt(self, mock_input):
        """Test KeyboardInterrupt returns None."""
        mock_input.side_effect = KeyboardInterrupt()
        result = get_user_input()
        assert result is None


class TestMain:
    """Test cases for main function."""
    
    @patch('sys.argv', ['roman.py', '42'])
    @patch('builtins.print')
    def test_command_line_valid_input(self, mock_print):
        """Test main with valid command-line argument."""
        main()
        mock_print.assert_called_once_with("42 in Roman numerals is: XLII")
    
    @patch('sys.argv', ['roman.py', '0'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_command_line_invalid_input(self, mock_exit, mock_print):
        """Test main with invalid command-line argument."""
        main()
        mock_print.assert_called_once()
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['roman.py', 'not_a_number'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_command_line_non_numeric_input(self, mock_exit, mock_print):
        """Test main with non-numeric command-line argument."""
        main()
        mock_print.assert_called_once()
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_mode_single_conversion(self, mock_print, mock_input, mock_get_input):
        """Test interactive mode with single conversion."""
        mock_get_input.return_value = 42
        mock_input.return_value = 'n'
        
        main()
        
        # Check that the conversion was printed
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        assert any("42 in Roman numerals is: XLII" in call for call in print_calls)
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_mode_invalid_input(self, mock_print, mock_input, mock_get_input):
        """Test interactive mode with invalid input."""
        mock_get_input.side_effect = [None, 42]  # First invalid, then valid
        mock_input.return_value = 'n'
        
        main()
        
        # Check that error message was printed
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        assert any("Invalid input" in call for call in print_calls)
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_mode_keyboard_interrupt(self, mock_print, mock_input, mock_get_input):
        """Test interactive mode with KeyboardInterrupt."""
        mock_get_input.side_effect = KeyboardInterrupt()
        
        main()
        
        # Check that goodbye message was printed
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        assert any("Goodbye!" in call for call in print_calls)
