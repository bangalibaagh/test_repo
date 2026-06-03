#!/usr/bin/env python3
"""
Test file for decimal_to_roman.py

Tests the Roman numeral conversion logic with various test cases.
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch

from decimal_to_roman import decimal_to_roman, main


class TestDecimalToRoman:
    """Test cases for decimal_to_roman function."""
    
    def test_basic_numbers(self):
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
    
    def test_tens(self):
        """Test numbers involving tens."""
        assert decimal_to_roman(10) == "X"
        assert decimal_to_roman(20) == "XX"
        assert decimal_to_roman(30) == "XXX"
        assert decimal_to_roman(40) == "XL"
        assert decimal_to_roman(50) == "L"
        assert decimal_to_roman(60) == "LX"
        assert decimal_to_roman(70) == "LXX"
        assert decimal_to_roman(80) == "LXXX"
        assert decimal_to_roman(90) == "XC"
    
    def test_hundreds(self):
        """Test numbers involving hundreds."""
        assert decimal_to_roman(100) == "C"
        assert decimal_to_roman(200) == "CC"
        assert decimal_to_roman(300) == "CCC"
        assert decimal_to_roman(400) == "CD"
        assert decimal_to_roman(500) == "D"
        assert decimal_to_roman(600) == "DC"
        assert decimal_to_roman(700) == "DCC"
        assert decimal_to_roman(800) == "DCCC"
        assert decimal_to_roman(900) == "CM"
    
    def test_thousands(self):
        """Test numbers involving thousands."""
        assert decimal_to_roman(1000) == "M"
        assert decimal_to_roman(2000) == "MM"
        assert decimal_to_roman(3000) == "MMM"
    
    def test_complex_numbers(self):
        """Test complex multi-digit numbers."""
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
    
    def test_edge_cases(self):
        """Test edge cases at boundaries."""
        assert decimal_to_roman(1) == "I"  # Minimum
        assert decimal_to_roman(3999) == "MMMCMXCIX"  # Maximum
    
    def test_famous_years(self):
        """Test some famous historical years."""
        assert decimal_to_roman(1776) == "MDCCLXXVI"  # American Independence
        assert decimal_to_roman(1969) == "MCMLXIX"  # Moon landing
        assert decimal_to_roman(2000) == "MM"  # Y2K
    
    def test_invalid_inputs(self):
        """Test invalid input handling."""
        with pytest.raises(ValueError):
            decimal_to_roman(0)
        
        with pytest.raises(ValueError):
            decimal_to_roman(-1)
        
        with pytest.raises(ValueError):
            decimal_to_roman(4000)
        
        with pytest.raises(ValueError):
            decimal_to_roman("not a number")
    
    def test_main_with_command_line_arg(self):
        """Test main function with command line argument."""
        with patch('sys.argv', ['decimal_to_roman.py', '42']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                assert "42 in Roman numerals is: XLII" in output
    
    def test_main_with_interactive_input(self):
        """Test main function with interactive input."""
        with patch('sys.argv', ['decimal_to_roman.py']):
            with patch('builtins.input', return_value='123'):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    main()
                    output = fake_out.getvalue()
                    assert "123 in Roman numerals is: CXXIII" in output
    
    def test_main_with_invalid_input(self):
        """Test main function with invalid input."""
        with patch('sys.argv', ['decimal_to_roman.py', 'invalid']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                with pytest.raises(SystemExit):
                    main()
                output = fake_out.getvalue()
                assert "Error: Please enter a valid integer." in output
    
    def test_main_with_out_of_range_input(self):
        """Test main function with out of range input."""
        with patch('sys.argv', ['decimal_to_roman.py', '5000']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                with pytest.raises(SystemExit):
                    main()
                output = fake_out.getvalue()
                assert "Error: Number must be an integer between 1 and 3999" in output