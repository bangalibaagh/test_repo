#!/usr/bin/env python3
"""
Tests for find_single_number.py
"""

import unittest
import subprocess
import sys
from find_single_number import find_single_number, parse_input


class TestFindSingleNumber(unittest.TestCase):
    """Test cases for the find_single_number function."""
    
    def test_basic_case(self):
        """Test basic case with one unique number."""
        nums = [1, 2, 3, 2, 1]
        result = find_single_number(nums)
        self.assertEqual(result, 3)
    
    def test_single_element(self):
        """Test with single element list."""
        nums = [42]
        result = find_single_number(nums)
        self.assertEqual(result, 42)
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        nums = [-1, -2, -3, -2, -1]
        result = find_single_number(nums)
        self.assertEqual(result, -3)
    
    def test_zero_in_list(self):
        """Test with zero in the list."""
        nums = [0, 1, 0, 2, 1]
        result = find_single_number(nums)
        self.assertEqual(result, 2)
    
    def test_empty_list(self):
        """Test that empty list raises ValueError."""
        with self.assertRaises(ValueError):
            find_single_number([])
    
    def test_larger_list(self):
        """Test with larger list."""
        nums = [1, 2, 3, 4, 5, 1, 2, 3, 4]
        result = find_single_number(nums)
        self.assertEqual(result, 5)


class TestParseInput(unittest.TestCase):
    """Test cases for the parse_input function."""
    
    def test_valid_input(self):
        """Test parsing valid comma-separated numbers."""
        result = parse_input("1,2,3,2,1")
        self.assertEqual(result, [1, 2, 3, 2, 1])
    
    def test_spaces_in_input(self):
        """Test parsing input with spaces."""
        result = parse_input("1, 2, 3, 2, 1")
        self.assertEqual(result, [1, 2, 3, 2, 1])
    
    def test_negative_numbers(self):
        """Test parsing negative numbers."""
        result = parse_input("-1,2,-3,2,-1")
        self.assertEqual(result, [-1, 2, -3, 2, -1])
    
    def test_single_number(self):
        """Test parsing single number."""
        result = parse_input("42")
        self.assertEqual(result, [42])
    
    def test_empty_string(self):
        """Test parsing empty string."""
        result = parse_input("")
        self.assertEqual(result, [])
    
    def test_whitespace_only(self):
        """Test parsing whitespace-only string."""
        result = parse_input("   ")
        self.assertEqual(result, [])
    
    def test_invalid_input(self):
        """Test that invalid input raises ValueError."""
        with self.assertRaises(ValueError):
            parse_input("1,2,abc,2,1")
    
    def test_invalid_input_with_special_chars(self):
        """Test that input with special characters raises ValueError."""
        with self.assertRaises(ValueError):
            parse_input("1,2,3@,2,1")


class TestScriptIntegration(unittest.TestCase):
    """Integration tests for the script."""
    
    def test_script_success(self):
        """Test script runs successfully with valid input."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py", "1,2,3,2,1"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "3")
    
    def test_script_no_args(self):
        """Test script exits with error when no arguments provided."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Usage:", result.stderr)
    
    def test_script_too_many_args(self):
        """Test script exits with error when too many arguments provided."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py", "1,2,3", "extra"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Usage:", result.stderr)
    
    def test_script_empty_input(self):
        """Test script exits with error for empty input."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py", ""],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error: Input list cannot be empty", result.stderr)
    
    def test_script_invalid_input(self):
        """Test script exits with error for invalid input."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py", "1,2,abc,2,1"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error:", result.stderr)
    
    def test_script_invalid_characters(self):
        """Test script exits with error for input with invalid characters."""
        result = subprocess.run(
            [sys.executable, "find_single_number.py", "1,2,3;rm -rf /"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error: Input contains invalid characters", result.stderr)


if __name__ == "__main__":
    unittest.main()
