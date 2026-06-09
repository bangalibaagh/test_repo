#!/usr/bin/env python3
"""Tests for the calculator script."""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

# Add the scripts directory to the path to import calculator
sys.path.insert(0, 'scripts')
from calculator import add_numbers, get_number_input, main


class TestAddNumbers:
    """Test cases for the add_numbers function."""
    
    def test_valid_input(self):
        """Test addition with valid integer inputs."""
        assert add_numbers(5, 3) == 8
        assert add_numbers(10, 20) == 30
        assert add_numbers(0, 0) == 0
    
    def test_complex_numbers(self):
        """Test addition with floating point numbers."""
        assert add_numbers(2.5, 3.7) == pytest.approx(6.2)
        assert add_numbers(1.1, 2.2) == pytest.approx(3.3)
        assert add_numbers(0.1, 0.2) == pytest.approx(0.3)
    
    def test_numbers_and_special_chars(self):
        """Test addition with negative numbers and edge cases."""
        assert add_numbers(-5, 3) == -2
        assert add_numbers(-10, -20) == -30
        assert add_numbers(5, -3) == 2
    
    def test_large_numbers(self):
        """Test addition with large numbers."""
        assert add_numbers(1000000, 2000000) == 3000000
        assert add_numbers(999999999, 1) == 1000000000
    
    def test_thousands(self):
        """Test addition with numbers in thousands range."""
        assert add_numbers(1000, 2000) == 3000
        assert add_numbers(5000, 7000) == 12000
        assert add_numbers(1500, 2500) == 4000


class TestGetNumberInput:
    """Test cases for the get_number_input function."""
    
    def test_valid_number_input(self):
        """Test valid number input parsing."""
        with patch('builtins.input', return_value='42'):
            result = get_number_input("Enter number: ")
            assert result == 42.0
    
    def test_invalid_number_input(self):
        """Test handling of invalid number input."""
        with patch('builtins.input', side_effect=['abc', '123']):
            with patch('builtins.print') as mock_print:
                result = get_number_input("Enter number: ")
                assert result == 123.0
                mock_print.assert_called_with("Error: Please enter a valid number.")
    
    def test_out_of_range_input(self):
        """Test handling of empty input."""
        with patch('builtins.input', side_effect=['', '456']):
            with patch('builtins.print') as mock_print:
                result = get_number_input("Enter number: ")
                assert result == 456.0
                mock_print.assert_called_with("Error: Input cannot be empty")
    
    def test_boundary_inputs(self):
        """Test boundary value inputs."""
        with patch('builtins.input', return_value='0'):
            result = get_number_input("Enter number: ")
            assert result == 0.0
        
        with patch('builtins.input', return_value='-1'):
            result = get_number_input("Enter number: ")
            assert result == -1.0


class TestMainFunction:
    """Test cases for the main function."""
    
    def test_cli_valid_numbers(self):
        """Test main function with valid number inputs."""
        with patch('builtins.input', side_effect=['10', '20']):
            with patch('builtins.print') as mock_print:
                main()
                # Check that result was printed
                calls = [str(call) for call in mock_print.call_args_list]
                assert any('30' in call for call in calls)
    
    def test_boundary_inputs_cli(self):
        """Test main function with boundary inputs."""
        with patch('builtins.input', side_effect=['0', '0']):
            with patch('builtins.print') as mock_print:
                main()
                calls = [str(call) for call in mock_print.call_args_list]
                assert any('0' in call for call in calls)
    
    def test_keyboard_interrupt(self):
        """Test handling of keyboard interrupt."""
        with patch('builtins.input', side_effect=KeyboardInterrupt()):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 0
                mock_print.assert_called_with("\n\nCalculation cancelled by user.")
    
    def test_floating_point_result(self):
        """Test main function with floating point result."""
        with patch('builtins.input', side_effect=['1.5', '2.7']):
            with patch('builtins.print') as mock_print:
                main()
                calls = [str(call) for call in mock_print.call_args_list]
                assert any('4.2' in call for call in calls)
