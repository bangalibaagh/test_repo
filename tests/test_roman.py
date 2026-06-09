#!/usr/bin/env python3
"""Tests for roman numeral converter."""

import pytest
import subprocess
import sys
from io import StringIO
from unittest.mock import patch

from scripts.roman import decimal_to_roman, main


class TestDecimalToRoman:
    """Test cases for decimal_to_roman function."""
    
    def test_single_digits(self):
        """Test conversion of single digit numbers."""
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
        """Test conversion of tens."""
        assert decimal_to_roman(10) == "X"
        assert decimal_to_roman(20) == "XX"
        assert decimal_to_roman(30) == "XXX"
        assert decimal_to_roman(40) == "XL"
        assert decimal_to_roman(50) == "L"
        assert decimal_to_roman(60) == "LX"
        assert decimal_to_roman(70) == "LXX"
        assert decimal_to_roman(80) == "LXXX"
        assert decimal_to_roman(90) == "XC"
    
    def test_complex_numbers(self):
        """Test conversion of complex multi-digit numbers."""
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
    
    def test_numbers_and_special_chars(self):
        """Test numbers with special character combinations."""
        assert decimal_to_roman(444) == "CDXLIV"
        assert decimal_to_roman(888) == "DCCCLXXXVIII"
        assert decimal_to_roman(999) == "CMXCIX"
        assert decimal_to_roman(1444) == "MCDXLIV"
        assert decimal_to_roman(1888) == "MDCCCLXXXVIII"
        assert decimal_to_roman(1999) == "MCMXCIX"
        assert decimal_to_roman(2444) == "MMCDXLIV"
        assert decimal_to_roman(2888) == "MMDCCCLXXXVIII"
        assert decimal_to_roman(2999) == "MMCMXCIX"
        assert decimal_to_roman(3444) == "MMMCDXLIV"
        assert decimal_to_roman(3888) == "MMMDCCCLXXXVIII"
        assert decimal_to_roman(3999) == "MMMCMXCIX"
    
    def test_large_numbers(self):
        """Test conversion of large numbers."""
        assert decimal_to_roman(100) == "C"
        assert decimal_to_roman(500) == "D"
        assert decimal_to_roman(1000) == "M"
        assert decimal_to_roman(1500) == "MD"
        assert decimal_to_roman(2000) == "MM"
        assert decimal_to_roman(3000) == "MMM"
        assert decimal_to_roman(3500) == "MMMD"
    
    def test_valid_input(self):
        """Test valid boundary inputs."""
        assert decimal_to_roman(1) == "I"
        assert decimal_to_roman(3999) == "MMMCMXCIX"
        assert decimal_to_roman(1994) == "MCMXCIV"
        assert decimal_to_roman(2021) == "MMXXI"
        assert decimal_to_roman(1776) == "MDCCLXXVI"
        assert decimal_to_roman(2023) == "MMXXIII"
    
    def test_hundreds(self):
        """Test conversion of hundreds."""
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
        """Test conversion of thousands."""
        assert decimal_to_roman(1000) == "M"
        assert decimal_to_roman(2000) == "MM"
        assert decimal_to_roman(3000) == "MMM"
    
    def test_invalid_number_input(self):
        """Test invalid number inputs."""
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(0)
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(-1)
        with pytest.raises(ValueError, match="Number must be an integer between 1 and 3999"):
            decimal_to_roman(4000)
    
    def test_out_of_range_input(self):
        """Test out of range inputs."""
        with pytest.raises(ValueError):
            decimal_to_roman(0)
        with pytest.raises(ValueError):
            decimal_to_roman(-5)
        with pytest.raises(ValueError):
            decimal_to_roman(4000)
        with pytest.raises(ValueError):
            decimal_to_roman(10000)
    
    def test_boundary_inputs_cli(self):
        """Test CLI with boundary inputs using subprocess integration."""
        # Test valid boundary cases
        result = subprocess.run([sys.executable, "scripts/roman.py", "1"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert result.stdout.strip() == "I"
        
        result = subprocess.run([sys.executable, "scripts/roman.py", "3999"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert result.stdout.strip() == "MMMCMXCIX"
        
        # Test invalid boundary cases
        result = subprocess.run([sys.executable, "scripts/roman.py", "0"], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert "Error:" in result.stderr
        
        result = subprocess.run([sys.executable, "scripts/roman.py", "4000"], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert "Error:" in result.stderr
    
    def test_cli_valid_numbers(self):
        """Test CLI with valid numbers using subprocess integration."""
        test_cases = [
            ("42", "XLII"),
            ("1994", "MCMXCIV"),
            ("2023", "MMXXIII"),
            ("500", "D"),
            ("1000", "M")
        ]
        
        for num_str, expected in test_cases:
            result = subprocess.run([sys.executable, "scripts/roman.py", num_str], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            assert result.stdout.strip() == expected
    
    def test_cli_invalid_arguments(self):
        """Test CLI with invalid arguments using subprocess integration."""
        # Test non-numeric input (argparse error)
        result = subprocess.run([sys.executable, "scripts/roman.py", "abc"], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        
        # Test no arguments (argparse error)
        result = subprocess.run([sys.executable, "scripts/roman.py"], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        
        # Test too many arguments (argparse error)
        result = subprocess.run([sys.executable, "scripts/roman.py", "42", "extra"], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        
        # Test float input (argparse error)
        result = subprocess.run([sys.executable, "scripts/roman.py", "42.5"], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        
        # Test help flag (argparse SystemExit with code 0, but we convert to 1)
        result = subprocess.run([sys.executable, "scripts/roman.py", "--help"], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        
        # Test negative number (ValueError, not argparse error)
        result = subprocess.run([sys.executable, "scripts/roman.py", "-5"], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert "Error:" in result.stderr
    
    def test_main_function_with_mock(self):
        """Test main function with mocked sys.argv."""
        with patch('sys.argv', ['roman.py', '42']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                assert mock_stdout.getvalue().strip() == "XLII"
        
        with patch('sys.argv', ['roman.py', '0']):
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "Error:" in mock_stderr.getvalue()
