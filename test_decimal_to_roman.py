import unittest
import sys
from io import StringIO
from unittest.mock import patch
from decimal_to_roman import decimal_to_roman, main


class TestDecimalToRoman(unittest.TestCase):
    def test_valid_conversions(self):
        """Test valid decimal to roman conversions"""
        test_cases = [
            (1, 'I'),
            (4, 'IV'),
            (5, 'V'),
            (9, 'IX'),
            (10, 'X'),
            (40, 'XL'),
            (50, 'L'),
            (90, 'XC'),
            (100, 'C'),
            (400, 'CD'),
            (500, 'D'),
            (900, 'CM'),
            (1000, 'M'),
            (1994, 'MCMXCIV'),
            (3999, 'MMMCMXCIX')
        ]
        
        for decimal, expected_roman in test_cases:
            with self.subTest(decimal=decimal):
                self.assertEqual(decimal_to_roman(decimal), expected_roman)
    
    def test_invalid_inputs(self):
        """Test invalid inputs to decimal_to_roman function"""
        with self.assertRaises(ValueError):
            decimal_to_roman(0)
        
        with self.assertRaises(ValueError):
            decimal_to_roman(-1)
        
        with self.assertRaises(ValueError):
            decimal_to_roman(4000)


class TestMainFunction(unittest.TestCase):
    """Test cases for main() function input handling"""
    
    @patch('sys.argv', ['script.py', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_valid_input(self, mock_stdout):
        """Test main function with valid integer input"""
        main()
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, 'XLII')
    
    @patch('sys.argv', ['script.py', 'invalid'])
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_invalid_string_input(self, mock_stdout, mock_stderr):
        """Test main function with invalid string input"""
        main()
        error_output = mock_stderr.getvalue()
        self.assertIn('Error: Invalid input', error_output)
        self.assertIn('invalid', error_output)
    
    @patch('sys.argv', ['script.py', '0'])
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_zero_input(self, mock_stdout, mock_stderr):
        """Test main function with zero input"""
        main()
        error_output = mock_stderr.getvalue()
        self.assertIn('Error:', error_output)
    
    @patch('sys.argv', ['script.py', '-5'])
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_negative_input(self, mock_stdout, mock_stderr):
        """Test main function with negative input"""
        main()
        error_output = mock_stderr.getvalue()
        self.assertIn('Error:', error_output)
    
    @patch('sys.argv', ['script.py', '4000'])
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_out_of_range_input(self, mock_stdout, mock_stderr):
        """Test main function with out of range input"""
        main()
        error_output = mock_stderr.getvalue()
        self.assertIn('Error:', error_output)
    
    @patch('sys.argv', ['script.py'])
    @patch('builtins.input', return_value='invalid_input')
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_args_invalid_stdin(self, mock_stdout, mock_stderr, mock_input):
        """Test main function with no args and invalid stdin input"""
        main()
        error_output = mock_stderr.getvalue()
        self.assertIn('Error: Invalid input', error_output)
        self.assertIn('invalid_input', error_output)
    
    @patch('sys.argv', ['script.py'])
    @patch('builtins.input', return_value='42')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_args_valid_stdin(self, mock_stdout, mock_input):
        """Test main function with no args and valid stdin input"""
        main()
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, 'XLII')


if __name__ == '__main__':
    unittest.main()
