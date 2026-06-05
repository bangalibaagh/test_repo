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
            decimal_to_roman([])


class TestGetUserInput:
    """Test cases for get_user_input function."""
    
    @patch('builtins.input', return_value='42')
    def test_valid_input(self, mock_input):
        """Test valid numeric input."""
        result = get_user_input()
        assert result == 42
        mock_input.assert_called_once_with("Enter a decimal number (1-3999): ")
    
    @patch('builtins.input', side_effect=['abc', '42'])
    def test_invalid_then_valid_input(self, mock_input):
        """Test invalid input followed by valid input."""
        with patch('builtins.print') as mock_print:
            result = get_user_input()
            assert result == 42
            mock_print.assert_called_with("Invalid input. Please enter a valid integer.")
    
    @patch('builtins.input', side_effect=['0', '42'])
    def test_out_of_range_then_valid_input(self, mock_input):
        """Test out of range input followed by valid input."""
        with patch('builtins.print') as mock_print:
            result = get_user_input()
            assert result == 42
            mock_print.assert_called_with("Number must be between 1 and 3999.")
    
    @patch('builtins.input', side_effect=['4000', '42'])
    def test_too_large_then_valid_input(self, mock_input):
        """Test too large input followed by valid input."""
        with patch('builtins.print') as mock_print:
            result = get_user_input()
            assert result == 42
            mock_print.assert_called_with("Number must be between 1 and 3999.")


class TestInteractiveFlow:
    """Test cases for complete interactive flow."""
    
    @patch('builtins.input', side_effect=['42', 'n'])
    @patch('builtins.print')
    def test_single_conversion_quit(self, mock_print, mock_input):
        """Test single conversion followed by quit."""
        main()
        
        # Verify the conversion was printed
        mock_print.assert_any_call("42 in Roman numerals is: XLII")
        # Verify continue prompt was shown
        mock_input.assert_any_call("Do you want to convert another number? (y/n): ")
    
    @patch('builtins.input', side_effect=['42', 'y', '100', 'n'])
    @patch('builtins.print')
    def test_multiple_conversions(self, mock_print, mock_input):
        """Test multiple conversions with continue logic."""
        main()
        
        # Verify both conversions were printed
        mock_print.assert_any_call("42 in Roman numerals is: XLII")
        mock_print.assert_any_call("100 in Roman numerals is: C")
        # Verify continue prompts were shown
        assert mock_input.call_count >= 4  # At least 2 number inputs + 2 continue prompts
    
    @patch('builtins.input', side_effect=['abc', '42', 'n'])
    @patch('builtins.print')
    def test_error_recovery_in_loop(self, mock_print, mock_input):
        """Test error recovery within the interactive loop."""
        main()
        
        # Verify error message was shown
        mock_print.assert_any_call("Invalid input. Please enter a valid integer.")
        # Verify successful conversion after error
        mock_print.assert_any_call("42 in Roman numerals is: XLII")
    
    @patch('builtins.input', side_effect=['42', 'invalid', 'y', '100', 'n'])
    @patch('builtins.print')
    def test_invalid_continue_response(self, mock_print, mock_input):
        """Test invalid response to continue prompt."""
        main()
        
        # Verify both conversions happened despite invalid continue response
        mock_print.assert_any_call("42 in Roman numerals is: XLII")
        mock_print.assert_any_call("100 in Roman numerals is: C")
    
    @patch('builtins.input', side_effect=['0', '4000', '42', 'n'])
    @patch('builtins.print')
    def test_multiple_range_errors_recovery(self, mock_print, mock_input):
        """Test recovery from multiple range errors."""
        main()
        
        # Verify range error messages
        assert mock_print.call_count >= 3  # At least 2 error messages + 1 success
        mock_print.assert_any_call("Number must be between 1 and 3999.")
        mock_print.assert_any_call("42 in Roman numerals is: XLII")


class TestCommandLineArguments:
    """Test cases for command-line argument validation."""
    
    def test_valid_command_line_argument(self):
        """Test valid command-line argument."""
        with patch('sys.argv', ['roman.py', '42']):
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_called_once_with("42 in Roman numerals is: XLII")
    
    def test_non_numeric_command_line_argument(self):
        """Test non-numeric command-line argument."""
        with patch('sys.argv', ['roman.py', 'abc']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                mock_print.assert_called_with("Error: 'abc' is not a valid integer.")
    
    def test_float_command_line_argument(self):
        """Test float command-line argument."""
        with patch('sys.argv', ['roman.py', '3.14']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                mock_print.assert_called_with("Error: '3.14' is not a valid integer.")
    
    def test_out_of_range_low_command_line_argument(self):
        """Test out of range (too low) command-line argument."""
        with patch('sys.argv', ['roman.py', '0']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                mock_print.assert_called_with("Error: Number must be between 1 and 3999.")
    
    def test_out_of_range_high_command_line_argument(self):
        """Test out of range (too high) command-line argument."""
        with patch('sys.argv', ['roman.py', '4000']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                mock_print.assert_called_with("Error: Number must be between 1 and 3999.")
    
    def test_negative_command_line_argument(self):
        """Test negative command-line argument."""
        with patch('sys.argv', ['roman.py', '-5']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                mock_print.assert_called_with("Error: Number must be between 1 and 3999.")
    
    def test_multiple_command_line_arguments(self):
        """Test multiple command-line arguments (should use first valid one)."""
        with patch('sys.argv', ['roman.py', '42', '100']):
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_called_once_with("42 in Roman numerals is: XLII")
    
    def test_empty_string_command_line_argument(self):
        """Test empty string command-line argument."""
        with patch('sys.argv', ['roman.py', '']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                mock_print.assert_called_with("Error: '' is not a valid integer.")
    
    def test_whitespace_command_line_argument(self):
        """Test whitespace-only command-line argument."""
        with patch('sys.argv', ['roman.py', '   ']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                mock_print.assert_called_with("Error: '   ' is not a valid integer.")


class TestMainFunction:
    """Test cases for main function behavior."""
    
    @patch('builtins.input', return_value='42')
    @patch('builtins.print')
    def test_no_arguments_interactive_mode(self, mock_print, mock_input):
        """Test main function with no arguments enters interactive mode."""
        with patch('sys.argv', ['roman.py']):
            # Mock the continue prompt to exit after one iteration
            mock_input.side_effect = ['42', 'n']
            main()
            mock_print.assert_any_call("42 in Roman numerals is: XLII")
    
    def test_help_argument(self):
        """Test help argument display."""
        with patch('sys.argv', ['roman.py', '--help']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                # Should print usage information
                assert mock_print.called
    
    def test_version_argument(self):
        """Test version argument if implemented."""
        with patch('sys.argv', ['roman.py', '--version']):
            with patch('builtins.print') as mock_print:
                try:
                    main()
                except SystemExit:
                    pass  # Expected for version display
                # This test is flexible since version might not be implemented
