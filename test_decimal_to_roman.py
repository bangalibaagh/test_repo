import unittest
from unittest.mock import patch
import sys
from io import StringIO
from decimal_to_roman import decimal_to_roman, main


class TestDecimalToRoman(unittest.TestCase):
    
    def test_basic_conversions(self):
        """Test basic decimal to roman conversions."""
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
    
    def test_invalid_range(self):
        """Test that numbers outside valid range raise ValueError."""
        invalid_numbers = [0, -1, 4000, 5000]
        
        for num in invalid_numbers:
            with self.subTest(num=num):
                with self.assertRaises(ValueError) as cm:
                    decimal_to_roman(num)
                self.assertIn("between 1 and 3999", str(cm.exception))
    
    def test_non_integer_types(self):
        """Test that non-integer types raise ValueError with appropriate message."""
        invalid_types = [3.14, "42", [1, 2, 3], None]
        
        for invalid_input in invalid_types:
            with self.subTest(input=invalid_input):
                with self.assertRaises(ValueError) as cm:
                    decimal_to_roman(invalid_input)
                self.assertIn("Input must be an integer", str(cm.exception))
    
    def test_boolean_type(self):
        """Test that boolean types raise ValueError."""
        with self.assertRaises(ValueError) as cm:
            decimal_to_roman(True)
        self.assertIn("Input must be an integer", str(cm.exception))
    
    @patch('builtins.input', return_value='42')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_interactive_valid_input(self, mock_stdout, mock_input):
        """Test main function with valid interactive input."""
        with patch('sys.argv', ['script_name']):
            main()
        output = mock_stdout.getvalue()
        self.assertIn("42 in Roman numerals is: XLII", output)
    
    @patch('builtins.input', return_value='0')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_interactive_invalid_input(self, mock_stdout, mock_input):
        """Test main function with invalid interactive input."""
        with patch('sys.argv', ['script_name']):
            main()
        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
    
    @patch('sys.argv', ['script_name', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_command_line_valid_argument(self, mock_stdout):
        """Test main function with valid command line argument."""
        main()
        output = mock_stdout.getvalue()
        self.assertIn("42 in Roman numerals is: XLII", output)
    
    @patch('sys.argv', ['script_name', '0'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_command_line_invalid_range(self, mock_stdout):
        """Test main function with command line argument outside valid range."""
        with self.assertRaises(SystemExit):
            main()
        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
        self.assertIn("between 1 and 3999", output)
    
    @patch('sys.argv', ['script_name', 'abc'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_command_line_non_numeric(self, mock_stdout):
        """Test main function with non-numeric command line argument."""
        with self.assertRaises(SystemExit):
            main()
        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
        self.assertIn("must be a valid integer", output)
    
    @patch('sys.argv', ['script_name', '3.14'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_command_line_float_string(self, mock_stdout):
        """Test main function with float string as command line argument."""
        with self.assertRaises(SystemExit):
            main()
        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
        self.assertIn("must be a valid integer", output)


if __name__ == '__main__':
    unittest.main()
