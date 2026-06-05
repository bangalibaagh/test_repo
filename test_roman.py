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
        
        # Test additional non-integer types
        with pytest.raises(ValueError):
            decimal_to_roman([1, 2, 3])
        
        with pytest.raises(ValueError):
            decimal_to_roman({"number": 42})


class TestGetUserInput:
    """Test cases for get_user_input function."""
    
    @patch('builtins.input', return_value='42')
    def test_valid_input(self, mock_input):
        """Test valid numeric input."""
        result = get_user_input()
        assert result == 42
        mock_input.assert_called_once_with("Enter a number (1-3999): ")
    
    @patch('builtins.input', side_effect=['invalid', '42'])
    @patch('builtins.print')
    def test_invalid_then_valid_input(self, mock_print, mock_input):
        """Test invalid input followed by valid input."""
        result = get_user_input()
        assert result == 42
        assert mock_input.call_count == 2
        mock_print.assert_called_with("Please enter a valid integer.")
    
    @patch('builtins.input', side_effect=['0', '42'])
    @patch('builtins.print')
    def test_out_of_range_then_valid_input(self, mock_print, mock_input):
        """Test out of range input followed by valid input."""
        result = get_user_input()
        assert result == 42
        assert mock_input.call_count == 2
        mock_print.assert_called_with("Number must be between 1 and 3999.")
    
    @patch('builtins.input', side_effect=['', '42'])
    @patch('builtins.print')
    def test_empty_then_valid_input(self, mock_print, mock_input):
        """Test empty input followed by valid input."""
        result = get_user_input()
        assert result == 42
        assert mock_input.call_count == 2
        mock_print.assert_called_with("Please enter a valid integer.")
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_input):
        """Test KeyboardInterrupt returns None."""
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input', side_effect=EOFError)
    def test_eof_error(self, mock_input):
        """Test EOFError returns None."""
        result = get_user_input()
        assert result is None


class TestMain:
    """Test cases for main function."""
    
    @patch('sys.argv', ['roman.py', '42'])
    @patch('builtins.print')
    def test_command_line_valid_argument(self, mock_print):
        """Test main with valid command line argument."""
        main()
        mock_print.assert_called_with("42 in Roman numerals is: XLII")
    
    @patch('sys.argv', ['roman.py', '1'])
    @patch('builtins.print')
    def test_command_line_minimum_value(self, mock_print):
        """Test main with minimum valid value."""
        main()
        mock_print.assert_called_with("1 in Roman numerals is: I")
    
    @patch('sys.argv', ['roman.py', '3999'])
    @patch('builtins.print')
    def test_command_line_maximum_value(self, mock_print):
        """Test main with maximum valid value."""
        main()
        mock_print.assert_called_with("3999 in Roman numerals is: MMMCMXCIX")
    
    @patch('sys.argv', ['roman.py', 'invalid'])
    @patch('builtins.print')
    def test_command_line_invalid_string(self, mock_print):
        """Test main with invalid string argument."""
        with pytest.raises(SystemExit):
            main()
        mock_print.assert_called_with("Error: Please provide a valid integer between 1 and 3999.")
    
    @patch('sys.argv', ['roman.py', '3.14'])
    @patch('builtins.print')
    def test_command_line_float_string(self, mock_print):
        """Test main with float string argument."""
        with pytest.raises(SystemExit):
            main()
        mock_print.assert_called_with("Error: Please provide a valid integer between 1 and 3999.")
    
    @patch('sys.argv', ['roman.py', '0'])
    @patch('builtins.print')
    def test_command_line_zero(self, mock_print):
        """Test main with zero argument."""
        with pytest.raises(SystemExit):
            main()
        mock_print.assert_called_with("Error: Please provide a valid integer between 1 and 3999.")
    
    @patch('sys.argv', ['roman.py', '-1'])
    @patch('builtins.print')
    def test_command_line_negative(self, mock_print):
        """Test main with negative argument."""
        with pytest.raises(SystemExit):
            main()
        mock_print.assert_called_with("Error: Please provide a valid integer between 1 and 3999.")
    
    @patch('sys.argv', ['roman.py', '4000'])
    @patch('builtins.print')
    def test_command_line_too_large(self, mock_print):
        """Test main with too large argument."""
        with pytest.raises(SystemExit):
            main()
        mock_print.assert_called_with("Error: Please provide a valid integer between 1 and 3999.")
    
    @patch('sys.argv', ['roman.py', '42', 'extra'])
    @patch('builtins.print')
    def test_command_line_too_many_args(self, mock_print):
        """Test main with too many arguments."""
        with pytest.raises(SystemExit):
            main()
        mock_print.assert_called_with("Usage: python roman.py [number]")
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input', return_value=42)
    @patch('builtins.input', return_value='n')
    @patch('builtins.print')
    def test_interactive_mode_single_conversion(self, mock_print, mock_input, mock_get_input):
        """Test interactive mode with single conversion."""
        main()
        
        # Verify conversion was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("42 in Roman numerals is: XLII" in call for call in print_calls)
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input', side_effect=[42, 100, None])
    @patch('builtins.input', side_effect=['y', 'n'])
    @patch('builtins.print')
    def test_interactive_mode_complete_flow_continue_then_quit(self, mock_print, mock_input, mock_get_input):
        """Test complete interactive flow: convert, continue, convert again, then quit."""
        main()
        
        # Verify both conversions were printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("42 in Roman numerals is: XLII" in call for call in print_calls)
        assert any("100 in Roman numerals is: C" in call for call in print_calls)
        
        # Verify continue prompt was shown (check input calls instead of print calls)
        input_calls = [str(call) for call in mock_input.call_args_list]
        assert len(input_calls) == 2  # Two continue prompts
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input', return_value=None)
    @patch('builtins.print')
    def test_interactive_mode_immediate_quit(self, mock_print, mock_get_input):
        """Test interactive mode with immediate quit (Ctrl+C or EOF)."""
        main()
        
        # Should exit gracefully without conversion
        print_calls = [str(call) for call in mock_print.call_args_list]
        conversion_calls = [call for call in print_calls if "in Roman numerals is:" in call]
        assert len(conversion_calls) == 0
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input', side_effect=[42, None])
    @patch('builtins.input', return_value='y')
    @patch('builtins.print')
    def test_interactive_mode_quit_on_second_input(self, mock_print, mock_input, mock_get_input):
        """Test interactive mode: convert once, continue, then quit on second input."""
        main()
        
        # Verify first conversion was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("42 in Roman numerals is: XLII" in call for call in print_calls)
        
        # Verify continue prompt was shown
        input_calls = [str(call) for call in mock_input.call_args_list]
        assert len(input_calls) == 1  # One continue prompt
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input', side_effect=[42, 100])
    @patch('builtins.input', side_effect=['y', 'n'])
    @patch('builtins.print')
    def test_interactive_mode_error_recovery(self, mock_print, mock_input, mock_get_input):
        """Test interactive mode handles errors and continues loop."""
        main()
        
        # Verify both conversions were printed despite any errors
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("42 in Roman numerals is: XLII" in call for call in print_calls)
        assert any("100 in Roman numerals is: C" in call for call in print_calls)
        
        # Verify the loop continued after first conversion
        assert len(mock_get_input.call_args_list) == 2
        assert len(mock_input.call_args_list) == 2