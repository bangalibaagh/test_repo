#!/usr/bin/env python3
"""
Test suite for decimal_to_roman.py

Tests the decimal to Roman numeral conversion functionality.
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch

from decimal_to_roman import decimal_to_roman, main


class TestDecimalToRoman:
    """Test cases for decimal_to_roman function."""
    
    def test_basic_conversions(self):
        """Test basic single digit conversions."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(2) == "II"
        assert decimal_to_roman(3) == "III"
        assert decimal_to_roman(4) == "IV"
        assert decimal_to_roman(5) == "V"
        assert decimal_to_roman(6) == "VI"
        assert decimal_to_roman(7) == "VII"
        assert decimal_to_roman(8) == "VIII"
        assert decimal_to_roman(9) == "IX"
    
    def test_tens_conversions(self):
        """Test conversions for tens."""
        assert decimal_to_roman(10) == "X"
        assert decimal_to_roman(20) == "XX"
        assert decimal_to_roman(30) == "XXX"
        assert decimal_to_roman(40) == "XL"
        assert decimal_to_roman(50) == "L"
        assert decimal_to_roman(60) == "LX"
        assert decimal_to_roman(70) == "LXX"
        assert decimal_to_roman(80) == "LXXX"
        assert decimal_to_roman(90) == "XC"
    
    def test_hundreds_conversions(self):
        """Test conversions for hundreds."""
        assert decimal_to_roman(100) == "C"
        assert decimal_to_roman(200) == "CC"
        assert decimal_to_roman(300) == "CCC"
        assert decimal_to_roman(400) == "CD"
        assert decimal_to_roman(500) == "D"
        assert decimal_to_roman(600) == "DC"
        assert decimal_to_roman(700) == "DCC"
        assert decimal_to_roman(800) == "DCCC"
        assert decimal_to_roman(900) == "CM"
    
    def test_thousands_conversions(self):
        """Test conversions for thousands."""
        assert decimal_to_roman(1000) == "M"
        assert decimal_to_roman(2000) == "MM"
        assert decimal_to_roman(3000) == "MMM"
    
    def test_complex_numbers(self):
        """Test complex multi-digit conversions."""
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
    
    def test_famous_years(self):
        """Test some famous historical years."""
        assert decimal_to_roman(1066) == "MLXVI"  # Battle of Hastings
        assert decimal_to_roman(1492) == "MCDXCII"  # Columbus
        assert decimal_to_roman(1776) == "MDCCLXXVI"  # American Independence
        assert decimal_to_roman(1969) == "MCMLXIX"  # Moon landing
    
    def test_boundary_values(self):
        """Test boundary values."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(3999) == "MMMCMXCIX"
    
    def test_invalid_inputs(self):
        """Test invalid inputs raise ValueError."""
        with pytest.raises(ValueError):
            decimal_to_roman(0)
        
        with pytest.raises(ValueError):
            decimal_to_roman(-1)
        
        with pytest.raises(ValueError):
            decimal_to_roman(4000)
        
        with pytest.raises(ValueError):
            decimal_to_roman("not a number")  # type: ignore


class TestMainFunction:
    """Test cases for main function."""
    
    @patch('builtins.input', return_value='42')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_input(self, mock_stdout, mock_input):
        """Test main function with user input."""
        main()
        output = mock_stdout.getvalue()
        assert "42 in Roman numerals is: XLII" in output
    
    @patch('sys.argv', ['decimal_to_roman.py', '123'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_command_line_arg(self, mock_stdout):
        """Test main function with command line argument."""
        main()
        output = mock_stdout.getvalue()
        assert "123 in Roman numerals is: CXXIII" in output
    
    @patch('builtins.input', return_value='invalid')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_invalid_input(self, mock_stdout, mock_input):
        """Test main function with invalid input."""
        with pytest.raises(SystemExit):
            main()
        output = mock_stdout.getvalue()
        assert "Error: Please enter a valid integer." in output
    
    @patch('builtins.input', return_value='5000')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_out_of_range_input(self, mock_stdout, mock_input):
        """Test main function with out of range input."""
        with pytest.raises(SystemExit):
            main()
        output = mock_stdout.getvalue()
        assert "Error: Number must be an integer between 1 and 3999" in output
