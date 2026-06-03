import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

# Import the main module
import decimal_to_roman

class TestDecimalToRoman(unittest.TestCase):
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    @patch('sys.stdout', new_callable=StringIO)
    def test_interactive_mode_keyboard_interrupt(self, mock_stdout, mock_input):
        """Test that KeyboardInterrupt is properly handled in interactive mode."""
        # This test verifies the main function handles KeyboardInterrupt gracefully
        # when running in interactive mode
        try:
            # Call the main function that should handle KeyboardInterrupt
            decimal_to_roman.main()
        except SystemExit:
            pass  # Expected behavior when KeyboardInterrupt is handled
        
        # Verify appropriate message is displayed
        output = mock_stdout.getvalue()
        self.assertIn('interrupted', output.lower())

if __name__ == '__main__':
    unittest.main()
