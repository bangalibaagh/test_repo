import unittest
from decimal_to_roman import decimal_to_roman


class TestDecimalToRoman(unittest.TestCase):
    
    def test_basic_conversions(self):
        """Test basic decimal to Roman numeral conversions."""
        test_cases = [
            (1, "I"),
            (2, "II"),
            (3, "III"),
            (4, "IV"),
            (5, "V"),
            (6, "VI"),
            (7, "VII"),
            (8, "VIII"),
            (9, "IX"),
            (10, "X")
        ]
        
        for decimal, expected_roman in test_cases:
            with self.subTest(decimal=decimal):
                self.assertEqual(decimal_to_roman(decimal), expected_roman)
    
    def test_tens_conversions(self):
        """Test conversions for multiples of ten."""
        test_cases = [
            (10, "X"),
            (20, "XX"),
            (30, "XXX"),
            (40, "XL"),
            (50, "L"),
            (60, "LX"),
            (70, "LXX"),
            (80, "LXXX"),
            (90, "XC"),
            (100, "C")
        ]
        
        for decimal, expected_roman in test_cases:
            with self.subTest(decimal=decimal):
                self.assertEqual(decimal_to_roman(decimal), expected_roman)
    
    def test_hundreds_conversions(self):
        """Test conversions for multiples of hundred."""
        test_cases = [
            (100, "C"),
            (200, "CC"),
            (300, "CCC"),
            (400, "CD"),
            (500, "D"),
            (600, "DC"),
            (700, "DCC"),
            (800, "DCCC"),
            (900, "CM"),
            (1000, "M")
        ]
        
        for decimal, expected_roman in test_cases:
            with self.subTest(decimal=decimal):
                self.assertEqual(decimal_to_roman(decimal), expected_roman)
    
    def test_complex_conversions(self):
        """Test complex decimal to Roman numeral conversions."""
        test_cases = [
            (27, "XXVII"),
            (48, "XLVIII"),
            (59, "LIX"),
            (93, "XCIII"),
            (141, "CXLI"),
            (163, "CLXIII"),
            (402, "CDII"),
            (575, "DLXXV"),
            (911, "CMXI"),
            (1024, "MXXIV"),
            (3000, "MMM")
        ]
        
        for decimal, expected_roman in test_cases:
            with self.subTest(decimal=decimal):
                self.assertEqual(decimal_to_roman(decimal), expected_roman)
    
    def test_edge_cases(self):
        """Test edge cases for decimal to Roman numeral conversion."""
        # Test minimum and maximum valid values
        self.assertEqual(decimal_to_roman(1), "I")
        self.assertEqual(decimal_to_roman(3999), "MMMCMXCIX")
    
    def test_invalid_inputs(self):
        """Test that invalid inputs raise ValueError."""
        # Test zero and negative numbers
        with self.assertRaises(ValueError):
            decimal_to_roman(0)
        
        with self.assertRaises(ValueError):
            decimal_to_roman(-1)
        
        with self.assertRaises(ValueError):
            decimal_to_roman(-10)
        
        # Test numbers too large
        with self.assertRaises(ValueError):
            decimal_to_roman(4000)
        
        with self.assertRaises(ValueError):
            decimal_to_roman(5000)
        
        # Test non-integer types
        with self.assertRaises(ValueError):
            decimal_to_roman("not a number")
        
        with self.assertRaises(ValueError):
            decimal_to_roman(3.14)
        
        with self.assertRaises(ValueError):
            decimal_to_roman(None)
        
        with self.assertRaises(ValueError):
            decimal_to_roman([])


if __name__ == '__main__':
    unittest.main()
