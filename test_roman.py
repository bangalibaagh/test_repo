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
            decimal_to_roman({"key": "value"})
        
        with pytest.raises(ValueError):
            decimal_to_roman(True)
        
        with pytest.raises(ValueError):
            decimal_to_roman(False)


class TestGetUserInput:
    """Test cases for get_user_input function."""
    
    @patch('builtins.input', return_value='42')
    def test_valid_input(self, mock_input):
        """Test valid integer input."""
        result = get_user_input()
        assert result == 42
    
    @patch('builtins.input', return_value='invalid')
    def test_invalid_input(self, mock_input):
        """Test invalid input returns None."""
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input', side_effect=EOFError)
    def test_eof_error(self, mock_input):
        """Test EOFError handling returns None."""
        result = get_user_input()
        assert result is None
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_input):
        """Test KeyboardInterrupt handling returns None."""
        result = get_user_input()
        assert result is None


class TestMain:
    """Test cases for main function."""
    
    @patch('sys.argv', ['roman.py', '42'])
    @patch('builtins.print')
    def test_command_line_valid_input(self, mock_print):
        """Test command-line mode with valid input."""
        main()
        mock_print.assert_called_once_with("42 in Roman numerals is: XLII")
    
    @patch('sys.argv', ['roman.py', '0'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_command_line_invalid_range(self, mock_exit, mock_print):
        """Test command-line mode with out-of-range input."""
        main()
        mock_print.assert_called_once()
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['roman.py', 'invalid'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_command_line_invalid_format(self, mock_exit, mock_print):
        """Test command-line mode with non-integer input."""
        main()
        mock_print.assert_called_once()
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['roman.py', '3.14'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_command_line_float_input(self, mock_exit, mock_print):
        """Test command-line mode with float input."""
        main()
        mock_print.assert_called_once()
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['roman.py', '4000'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_command_line_out_of_range_high(self, mock_exit, mock_print):
        """Test command-line mode with number too high."""
        main()
        mock_print.assert_called_once()
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['roman.py', '-5'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_command_line_negative_input(self, mock_exit, mock_print):
        """Test command-line mode with negative input."""
        main()
        mock_print.assert_called_once()
        mock_exit.assert_called_once_with(1)
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input', side_effect=[42, None])
    @patch('builtins.input', return_value='n')
    @patch('builtins.print')
    def test_interactive_mode(self, mock_print, mock_input, mock_get_input):
        """Test interactive mode with valid input."""
        main()
        # Check that conversion was printed
        assert any("42 in Roman numerals is: XLII" in str(call) for call in mock_print.call_args_list)
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input', side_effect=KeyboardInterrupt)
    @patch('builtins.print')
    def test_interactive_keyboard_interrupt(self, mock_print, mock_get_input):
        """Test interactive mode with KeyboardInterrupt."""
        main()
        # Check that goodbye message was printed
        assert any("Goodbye!" in str(call) for call in mock_print.call_args_list)
    
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
        
        # Verify continue prompt was shown
        assert any("Do you want to convert another number?" in call for call in print_calls)
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input', side_effect=[None, 50, None])
    @patch('builtins.input', side_effect=['y', 'n'])
    @patch('builtins.print')
    def test_interactive_mode_error_recovery(self, mock_print, mock_input, mock_get_input):
        """Test interactive mode error recovery: invalid input, then valid input."""
        main()
        
        # Verify valid conversion was printed after error
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("50 in Roman numerals is: L" in call for call in print_calls)
        
        # Verify continue prompt was shown
        assert any("Do you want to convert another number?" in call for call in print_calls)
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input', side_effect=[42])
    @patch('builtins.input', return_value='n')
    @patch('builtins.print')
    def test_interactive_mode_quit_after_first_conversion(self, mock_print, mock_input, mock_get_input):
        """Test interactive mode: convert once then quit immediately."""
        main()
        
        # Verify conversion was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("42 in Roman numerals is: XLII" in call for call in print_calls)
        
        # Verify continue prompt was shown
        assert any("Do you want to convert another number?" in call for call in print_calls)
    
    @patch('sys.argv', ['roman.py'])
    @patch('roman.get_user_input', side_effect=[None, None, None])
    @patch('builtins.input', side_effect=['y', 'y', 'n'])
    @patch('builtins.print')
    def test_interactive_mode_multiple_errors_then_quit(self, mock_print, mock_input, mock_get_input):
        """Test interactive mode: multiple invalid inputs with continues, then quit."""
        main()
        
        # Verify continue prompts were shown multiple times
        print_calls = [str(call) for call in mock_print.call_args_list]
        continue_prompts = [call for call in print_calls if "Do you want to convert another number?" in call]
        assert len(continue_prompts) >= 2  # Should have multiple continue prompts
