import unittest
from find_single_number import find_single_number


class TestFindSingleNumber(unittest.TestCase):
    
    def test_basic_case(self):
        """Test basic case with one single number"""
        self.assertEqual(find_single_number([2, 2, 1]), 1)
        self.assertEqual(find_single_number([4, 1, 2, 1, 2]), 4)
        self.assertEqual(find_single_number([1]), 1)
    
    def test_larger_array(self):
        """Test with larger arrays"""
        self.assertEqual(find_single_number([1, 2, 3, 2, 1]), 3)
        self.assertEqual(find_single_number([5, 7, 5, 4, 7]), 4)
    
    def test_negative_numbers(self):
        """Test with negative numbers"""
        self.assertEqual(find_single_number([-1, -1, -2]), -2)
        self.assertEqual(find_single_number([3, -3, 3, -3, 5]), 5)
    
    def test_zero_in_array(self):
        """Test with zero in the array"""
        self.assertEqual(find_single_number([0, 1, 0]), 1)
        self.assertEqual(find_single_number([0]), 0)
    
    def test_empty_array(self):
        """Test with empty array"""
        with self.assertRaises(ValueError):
            find_single_number([])
    
    def test_multiple_unique_numbers(self):
        """Test XOR algorithm edge case: multiple numbers appearing once"""
        with self.assertRaises(ValueError) as cm:
            find_single_number([1, 2, 3])  # All appear once
        self.assertIn("Multiple numbers", str(cm.exception))
        
        with self.assertRaises(ValueError) as cm:
            find_single_number([1, 2, 2, 3, 3, 4])  # Two numbers appear once
        self.assertIn("Multiple numbers", str(cm.exception))
    
    def test_number_appears_three_times(self):
        """Test XOR algorithm edge case: number appearing 3+ times"""
        with self.assertRaises(ValueError) as cm:
            find_single_number([1, 1, 1])  # One number appears 3 times
        self.assertIn("appears 3 times", str(cm.exception))
        
        with self.assertRaises(ValueError) as cm:
            find_single_number([2, 2, 2, 3, 3])  # One appears 3 times, one appears twice
        self.assertIn("appears 3 times", str(cm.exception))
    
    def test_number_appears_five_times(self):
        """Test XOR algorithm edge case: number appearing 5 times"""
        with self.assertRaises(ValueError) as cm:
            find_single_number([1, 1, 1, 1, 1])  # One number appears 5 times
        self.assertIn("appears 5 times", str(cm.exception))
    
    def test_no_single_numbers(self):
        """Test constraint violation: no numbers appear exactly once"""
        with self.assertRaises(ValueError) as cm:
            find_single_number([1, 1, 2, 2])  # All appear twice
        self.assertIn("No number appears exactly once", str(cm.exception))
        
        with self.assertRaises(ValueError) as cm:
            find_single_number([3, 3, 3, 4, 4, 4])  # All appear 3 times
        self.assertIn("appears 3 times", str(cm.exception))
    
    def test_mixed_constraint_violations(self):
        """Test mixed constraint violations"""
        with self.assertRaises(ValueError) as cm:
            find_single_number([1, 1, 1, 2, 3])  # One appears 3 times, two appear once
        self.assertIn("appears 3 times", str(cm.exception))


if __name__ == '__main__':
    unittest.main()
