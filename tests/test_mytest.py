#!/usr/bin/env python3
"""Tests for the mytest.py script."""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the scripts directory to the path so we can import mytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import mytest


class TestSortNumbers:
    """Test cases for the sort_numbers function."""
    
    def test_sort_positive_numbers(self):
        """Test sorting positive numbers."""
        numbers = [5.0, 2.0, 8.0, 1.0, 9.0, 3.0, 7.0, 4.0, 6.0, 10.0]
        expected = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        result = mytest.sort_numbers(numbers)
        assert result == expected
    
    def test_sort_negative_numbers(self):
        """Test sorting negative numbers."""
        numbers = [-1.0, -5.0, -3.0, -2.0, -4.0, -10.0, -6.0, -7.0, -8.0, -9.0]
        expected = [-10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0]
        result = mytest.sort_numbers(numbers)
        assert result == expected
    
    def test_sort_mixed_numbers(self):
        """Test sorting mixed positive and negative numbers."""
        numbers = [5.0, -2.0, 8.0, -1.0, 0.0, 3.0, -7.0, 4.0, -6.0, 10.0]
        expected = [-7.0, -6.0, -2.0, -1.0, 0.0, 3.0, 4.0, 5.0, 8.0, 10.0]
        result = mytest.sort_numbers(numbers)
        assert result == expected
    
    def test_sort_decimal_numbers(self):
        """Test sorting decimal numbers."""
        numbers = [5.5, 2.1, 8.9, 1.2, 9.7, 3.3, 7.8, 4.4, 6.6, 10.0]
        expected = [1.2, 2.1, 3.3, 4.4, 5.5, 6.6, 7.8, 8.9, 9.7, 10.0]
        result = mytest.sort_numbers(numbers)
        assert result == expected
    
    def test_sort_duplicate_numbers(self):
        """Test sorting numbers with duplicates."""
        numbers = [5.0, 2.0, 5.0, 1.0, 2.0, 3.0, 1.0, 4.0, 3.0, 4.0]
        expected = [1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 4.0, 4.0, 5.0, 5.0]
        result = mytest.sort_numbers(numbers)
        assert result == expected
    
    def test_sort_already_sorted(self):
        """Test sorting already sorted numbers."""
        numbers = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        expected = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        result = mytest.sort_numbers(numbers)
        assert result == expected
    
    def test_sort_reverse_sorted(self):
        """Test sorting reverse sorted numbers."""
        numbers = [10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0]
        expected = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        result = mytest.sort_numbers(numbers)
        assert result == expected
    
    def test_sort_empty_list(self):
        """Test sorting empty list."""
        numbers = []
        expected = []
        result = mytest.sort_numbers(numbers)
        assert result == expected
    
    def test_sort_single_number(self):
        """Test sorting single number."""
        numbers = [42.0]
        expected = [42.0]
        result = mytest.sort_numbers(numbers)
        assert result == expected


class TestGetNumbers:
    """Test cases for the get_numbers function."""
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_numbers_valid_input(self, mock_print, mock_input):
        """Test getting 10 valid numbers from input."""
        mock_input.side_effect = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        result = mytest.get_numbers()
        expected = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        assert result == expected
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_numbers_with_invalid_input(self, mock_print, mock_input):
        """Test getting numbers with some invalid input."""
        mock_input.side_effect = ['1', 'abc', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        result = mytest.get_numbers()
        expected = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        assert result == expected
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_numbers_decimal_input(self, mock_print, mock_input):
        """Test getting decimal numbers from input."""
        mock_input.side_effect = ['1.5', '2.7', '3.1', '4.9', '5.2', '6.8', '7.3', '8.6', '9.4', '10.1']
        result = mytest.get_numbers()
        expected = [1.5, 2.7, 3.1, 4.9, 5.2, 6.8, 7.3, 8.6, 9.4, 10.1]
        assert result == expected


class TestMain:
    """Test cases for the main function."""
    
    @patch('mytest.get_numbers')
    @patch('builtins.print')
    def test_main_successful_execution(self, mock_print, mock_get_numbers):
        """Test successful execution of main function."""
        mock_get_numbers.return_value = [5.0, 2.0, 8.0, 1.0, 9.0, 3.0, 7.0, 4.0, 6.0, 10.0]
        
        mytest.main()
        
        # Verify that print was called with the expected output
        mock_print.assert_any_call("\nOriginal numbers:", [5.0, 2.0, 8.0, 1.0, 9.0, 3.0, 7.0, 4.0, 6.0, 10.0])
        mock_print.assert_any_call("Sorted numbers (lowest to highest):", [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    
    @patch('mytest.get_numbers')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_keyboard_interrupt(self, mock_exit, mock_print, mock_get_numbers):
        """Test main function handling KeyboardInterrupt."""
        mock_get_numbers.side_effect = KeyboardInterrupt()
        
        mytest.main()
        
        mock_print.assert_called_with("\nProgram interrupted by user.")
        mock_exit.assert_called_with(1)
    
    @patch('mytest.get_numbers')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_general_exception(self, mock_exit, mock_print, mock_get_numbers):
        """Test main function handling general exception."""
        mock_get_numbers.side_effect = Exception("Test error")
        
        mytest.main()
        
        mock_print.assert_called_with("An error occurred: Test error")
        mock_exit.assert_called_with(1)
