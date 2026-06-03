#!/usr/bin/env python3
"""
Tests for find_single_number.py script.
"""

import pytest
import subprocess
import sys
from find_single_number import find_single_number, parse_input


class TestFindSingleNumber:
    """Test cases for the find_single_number function."""
    
    def test_basic_case(self):
        """Test basic case with small numbers."""
        numbers = [1, 2, 1, 3, 2]
        assert find_single_number(numbers) == 3
    
    def test_single_element(self):
        """Test with only one element."""
        numbers = [42]
        assert find_single_number(numbers) == 42
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        numbers = [-1, 2, -1, 3, 2]
        assert find_single_number(numbers) == 3
    
    def test_zero_in_list(self):
        """Test with zero in the list."""
        numbers = [0, 1, 0, 2, 1]
        assert find_single_number(numbers) == 2
    
    def test_zero_is_single(self):
        """Test when zero is the single number."""
        numbers = [1, 2, 1, 0, 2]
        assert find_single_number(numbers) == 0
    
    def test_large_numbers(self):
        """Test with large numbers."""
        numbers = [1000000, 999999, 1000000, 123456, 999999]
        assert find_single_number(numbers) == 123456
    
    def test_many_pairs(self):
        """Test with many pairs and one single number."""
        numbers = [1, 2, 3, 4, 5, 1, 2, 3, 4, 99, 5]
        assert find_single_number(numbers) == 99


class TestParseInput:
    """Test cases for the parse_input function."""
    
    def test_valid_input(self):
        """Test parsing valid comma-separated numbers."""
        input_str = "1,2,1,3,2"
        expected = [1, 2, 1, 3, 2]
        assert parse_input(input_str) == expected
    
    def test_spaces_in_input(self):
        """Test parsing input with spaces."""
        input_str = "1, 2, 1, 3, 2"
        expected = [1, 2, 1, 3, 2]
        assert parse_input(input_str) == expected
    
    def test_negative_numbers_input(self):
        """Test parsing negative numbers."""
        input_str = "-1,2,-1,3,2"
        expected = [-1, 2, -1, 3, 2]
        assert parse_input(input_str) == expected
    
    def test_single_number_input(self):
        """Test parsing single number."""
        input_str = "42"
        expected = [42]
        assert parse_input(input_str) == expected
    
    def test_invalid_input(self):
        """Test parsing invalid input raises ValueError."""
        with pytest.raises(ValueError):
            parse_input("1,2,abc,3,2")
    
    def test_empty_values(self):
        """Test parsing input with empty values raises ValueError."""
        with pytest.raises(ValueError):
            parse_input("1,2,,3,2")


class TestScriptExecution:
    """Test cases for running the script as a command."""
    
    def test_command_line_argument(self):
        """Test script with command line argument."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py", "1,2,1,3,2"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "3"
    
    def test_stdin_input(self):
        """Test script with stdin input."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py"],
            input="1,2,1,3,2\n",
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "3"
    
    def test_negative_numbers_script(self):
        """Test script with negative numbers."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py", "-1,2,-1,3,2"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "3"
    
    def test_single_number_script(self):
        """Test script with single number."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py", "42"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "42"
    
    def test_invalid_input_script(self):
        """Test script with invalid input returns error."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py", "1,2,abc,3,2"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr
    
    def test_empty_input_script(self):
        """Test script with empty input returns error."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py", ""],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr
    
    def test_no_input_script(self):
        """Test script with no input and no stdin returns error."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py"],
            input="",
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr


if __name__ == "__main__":
    pytest.main([__file__])
