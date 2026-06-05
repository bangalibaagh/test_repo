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
        
        with pytest.raises(ValueError):
            decimal_to_roman(None)


class TestGetUserInput:
    """Test cases for get_user_input function."""
    
    @patch('builtins.input', return_value='42')
    def test_valid_input(self, mock_input):
        """Test valid integer input."""
        result = get_user_input()
        assert result == 42
    
    @patch('builtins.input', return_value='  123  ')
    def test_input_with_whitespace(self, mock_input):
        """Test input with surrounding whitespace."""
        result = get_user_input()
        assert result == 123
    
    @patch('builtins.input', return_value='abc')
    def test_invalid_string_input(self, mock_input):
        """Test invalid string input returns None."""
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input', return_value='3.14')
    def test_float_input(self, mock_input):
        """Test float input returns None."""
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input', side_effect=EOFError)
    def test_eof_error(self, mock_input):
        """Test EOFError returns None."""
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_input):
        """Test KeyboardInterrupt returns None."""
        result = get_user_input()
        assert result is None


class TestMain:
    """Test cases for main function."""
    
    @patch('sys.argv', ['roman.py', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_command_line_valid_argument(self, mock_stdout):
        """Test main with valid command-line argument."""
        main()
        output = mock_stdout.getvalue()
        assert "42 = XLII" in output
    
    @patch('sys.argv', ['roman.py', '0'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_command_line_invalid_argument(self, mock_stderr):
        """Test main with invalid command-line argument."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        assert "Error:" in mock_stderr.getvalue()
    
    @patch('sys.argv', ['roman.py', 'abc'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_command_line_non_integer_argument(self, mock_stderr):
        """Test main with non-integer command-line argument."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        assert "Error:" in mock_stderr.getvalue()
    
    @patch('sys.argv', ['roman.py', '1', '2', '3'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_too_many_arguments(self, mock_stderr):
        """Test main with too many command-line arguments."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        assert "Usage:" in mock_stderr.getvalue()
    
    @patch('sys.argv', ['roman.py'])
    @patch('builtins.input', side_effect=['42', KeyboardInterrupt])
    @patch('sys.stdout', new_callable=StringIO)
    def test_interactive_mode_valid_input(self, mock_stdout, mock_input):
        """Test interactive mode with valid input."""
        main()
        output = mock_stdout.getvalue()
        assert "42 = XLII" in output
        assert "Goodbye!" in output
    
    @patch('sys.argv', ['roman.py'])
    @patch('builtins.input', side_effect=['abc', '42', KeyboardInterrupt])
    @patch('sys.stdout', new_callable=StringIO)
    def test_interactive_mode_invalid_then_valid(self, mock_stdout, mock_input):
        """Test interactive mode with invalid then valid input."""
        main()
        output = mock_stdout.getvalue()
        assert "Invalid input" in output
        assert "42 = XLII" in output
    
    @patch('sys.argv', ['roman.py'])
    @patch('builtins.input', side_effect=['4000', KeyboardInterrupt])
    @patch('sys.stdout', new_callable=StringIO)
    def test_interactive_mode_out_of_range(self, mock_stdout, mock_input):
        """Test interactive mode with out-of-range input."""
        main()
        output = mock_stdout.getvalue()
        assert "Error:" in output
    
    @patch('sys.argv', ['roman.py'])
    @patch('builtins.input', side_effect=EOFError)
    @patch('sys.stdout', new_callable=StringIO)
    def test_interactive_mode_eof(self, mock_stdout, mock_input):
        """Test interactive mode with EOF."""
        main()
        output = mock_stdout.getvalue()
        assert "Goodbye!" in output


if __name__ == "__main__":
    pytest.main([__file__])
