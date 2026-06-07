#!/usr/bin/env python3
"""Tests for the wordcount module."""

import pytest
from scripts.wordcount import count_words


class TestCountWords:
    """Test cases for the count_words function."""
    
    def test_empty_string(self):
        """Test that empty string returns empty dict."""
        result = count_words("")
        assert result == {}
    
    def test_single_word(self):
        """Test counting a single word."""
        result = count_words("hello")
        assert result == {"hello": 1}
    
    def test_multiple_words(self):
        """Test counting multiple different words."""
        result = count_words("hello world python")
        expected = {"hello": 1, "world": 1, "python": 1}
        assert result == expected
    
    def test_repeated_words(self):
        """Test counting repeated words."""
        result = count_words("hello hello world hello")
        expected = {"hello": 3, "world": 1}
        assert result == expected
    
    def test_case_insensitivity(self):
        """Test that words are counted case-insensitively."""
        result = count_words("Hello HELLO hello World WORLD")
        expected = {"hello": 3, "world": 2}
        assert result == expected
    
    def test_punctuation_handling(self):
        """Test that punctuation is properly handled."""
        result = count_words("Hello, world! How are you? Fine, thanks.")
        expected = {
            "hello": 1,
            "world": 1,
            "how": 1,
            "are": 1,
            "you": 1,
            "fine": 1,
            "thanks": 1
        }
        assert result == expected
    
    def test_mixed_punctuation_and_case(self):
        """Test combination of punctuation and case variations."""
        result = count_words("Hello, Hello! WORLD. world?")
        expected = {"hello": 2, "world": 2}
        assert result == expected
    
    def test_numbers_and_words(self):
        """Test that numbers are treated as words."""
        result = count_words("I have 5 cats and 10 dogs")
        expected = {
            "i": 1,
            "have": 1,
            "5": 1,
            "cats": 1,
            "and": 1,
            "10": 1,
            "dogs": 1
        }
        assert result == expected
    
    def test_whitespace_variations(self):
        """Test various whitespace characters."""
        result = count_words("hello\tworld\nhello\r\nworld")
        expected = {"hello": 2, "world": 2}
        assert result == expected
    
    def test_only_punctuation(self):
        """Test string with only punctuation."""
        result = count_words("!@#$%^&*()")
        assert result == {}
    
    def test_contractions(self):
        """Test handling of contractions.
        
        Contractions should be treated as single words to preserve semantic meaning.
        """
        result = count_words("don't can't won't")
        expected = {"don't": 1, "can't": 1, "won't": 1}
        assert result == expected
    
    def test_hyphenated_words(self):
        """Test handling of hyphenated words."""
        result = count_words("well-known twenty-one state-of-the-art")
        expected = {"well-known": 1, "twenty-one": 1, "state-of-the-art": 1}
        assert result == expected
    
    def test_none_input(self):
        """Test that None input is handled properly."""
        with pytest.raises(TypeError):
            count_words(None)
    
    def test_non_string_inputs(self):
        """Test that non-string inputs raise TypeError."""
        with pytest.raises(TypeError):
            count_words(123)
        
        with pytest.raises(TypeError):
            count_words(["hello", "world"])
        
        with pytest.raises(TypeError):
            count_words({"hello": 1})
        
        with pytest.raises(TypeError):
            count_words(42.5)
    
    def test_unicode_characters(self):
        """Test handling of Unicode and non-ASCII characters."""
        result = count_words("café naïve résumé")
        expected = {"café": 1, "naïve": 1, "résumé": 1}
        assert result == expected
        
        # Test with mixed ASCII and Unicode
        result = count_words("hello café world naïve")
        expected = {"hello": 1, "café": 1, "world": 1, "naïve": 1}
        assert result == expected
    
    def test_very_long_string(self):
        """Test performance and behavior with very long input strings."""
        # Create a long string with repeated words
        long_text = " ".join(["word"] * 10000)
        result = count_words(long_text)
        expected = {"word": 10000}
        assert result == expected
        
        # Test with many unique words
        unique_words = [f"word{i}" for i in range(1000)]
        long_unique_text = " ".join(unique_words)
        result = count_words(long_unique_text)
        assert len(result) == 1000
        assert all(count == 1 for count in result.values())
    
    def test_extremely_long_single_word(self):
        """Test handling of individual words that are extremely long."""
        # Test a single very long word
        long_word = "a" * 1000
        result = count_words(long_word)
        expected = {long_word: 1}
        assert result == expected
        
        # Test multiple very long words
        long_words = ["x" * 500, "y" * 500, "z" * 500]
        long_text = " ".join(long_words)
        result = count_words(long_text)
        expected = {word: 1 for word in long_words}
        assert result == expected
