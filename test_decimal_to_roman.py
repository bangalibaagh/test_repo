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
    
    def test_edge_cases(self):
        """Test edge cases for valid range."""
        self.assertEqual(decimal_to_roman(1), 'I')
        self.assertEqual(decimal_to_roman(3999), 'MMMCMXCIX')
    
    def test_invalid_range(self):
        """Test numbers outside valid range."""
        with self.assertRaises(ValueError) as cm:
            decimal_to_roman(0)
        self.assertIn("Number must be between 1 and 3999", str(cm.exception))
        
        with self.assertRaises(ValueError) as cm:
            decimal_to_roman(4000)
        self.assertIn("Number must be between 1 and 3999", str(cm.exception))
        
        with self.assertRaises(ValueError) as cm:
            decimal_to_roman(-5)
        self.assertIn("Number must be between 1 and 3999", str(cm.exception))
    
    def test_invalid_types(self):
        """Test invalid input types."""
        with self.assertRaises(TypeError) as cm:
            decimal_to_roman("42")
        self.assertIn("Input must be an integer", str(cm.exception))
        
        with self.assertRaises(TypeError) as cm:
            decimal_to_roman(42.5)
        self.assertIn("Input must be an integer", str(cm.exception))
        
        with self.assertRaises(TypeError) as cm:
            decimal_to_roman(None)
        self.assertIn("Input must be an integer", str(cm.exception))


class TestMainFunction(unittest.TestCase):
    
    def test_command_line_valid_input(self):
        """Test main function with valid command line input."""
        with patch('sys.argv', ['script.py', '42']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("42 in Roman numerals is: XLII", output)
    
    def test_command_line_invalid_string_input(self):
        """Test main function with invalid string input via command line."""
        with patch('sys.argv', ['script.py', 'abc']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("Error: 'abc' is not a valid integer", output)
    
    def test_command_line_float_string_input(self):
        """Test main function with float string input via command line."""
        with patch('sys.argv', ['script.py', '3.14']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("Error: '3.14' is not a valid integer", output)
    
    def test_command_line_out_of_range(self):
        """Test main function with out of range input via command line."""
        with patch('sys.argv', ['script.py', '4000']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("Error: Number must be between 1 and 3999", output)
    
    @patch('builtins.input', return_value='42')
    def test_interactive_valid_input(self, mock_input):
        """Test main function with valid interactive input."""
        with patch('sys.argv', ['script.py']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("42 in Roman numerals is: XLII", output)
    
    @patch('builtins.input', return_value='abc')
    def test_interactive_invalid_string_input(self, mock_input):
        """Test main function with invalid string input in interactive mode."""
        with patch('sys.argv', ['script.py']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("Error: 'abc' is not a valid integer", output)
    
    @patch('builtins.input', return_value='3.14')
    def test_interactive_float_string_input(self, mock_input):
        """Test main function with float string input in interactive mode."""
        with patch('sys.argv', ['script.py']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("Error: '3.14' is not a valid integer", output)
    
    @patch('builtins.input', return_value='4000')
    def test_interactive_out_of_range(self, mock_input):
        """Test main function with out of range input in interactive mode."""
        with patch('sys.argv', ['script.py']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("Error: Number must be between 1 and 3999", output)
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_interactive_keyboard_interrupt(self, mock_input):
        """Test main function handles KeyboardInterrupt in interactive mode."""
        with patch('sys.argv', ['script.py']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("Goodbye!", output)


if __name__ == '__main__':
    unittest.main()
