#!/usr/bin/env python3
"""Tests for the wordcount module."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        result = count_words("well-known state-of-the-art")
        expected = {"well-known": 1, "state-of-the-art": 1}
        assert result == expected
    
    def test_none_input(self):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError, match="Input text cannot be None"):
            count_words(None)
    
    def test_non_string_input_types(self):
        """Test that non-string input types raise TypeError."""
        with pytest.raises(TypeError, match="Input must be a string"):
            count_words(123)
        
        with pytest.raises(TypeError, match="Input must be a string"):
            count_words(["hello", "world"])
        
        with pytest.raises(TypeError, match="Input must be a string"):
            count_words({"hello": 1})
        
        with pytest.raises(TypeError, match="Input must be a string"):
            count_words(True)
    
    def test_unicode_characters(self):
        """Test handling of unicode characters."""
        result = count_words("café naïve résumé")
        expected = {"café": 1, "naïve": 1, "résumé": 1}
        assert result == expected
    
    def test_mixed_unicode_and_ascii(self):
        """Test mixing unicode and ASCII characters."""
        result = count_words("hello café world naïve")
        expected = {"hello": 1, "café": 1, "world": 1, "naïve": 1}
        assert result == expected
    
    def test_emoji_handling(self):
        """Test that emojis are not counted as words."""
        result = count_words("hello 😀 world 🌍")
        expected = {"hello": 1, "world": 1}
        assert result == expected
    
    def test_input_length_limit(self):
        """Test that input longer than 100,000 characters raises ValueError."""
        long_text = "a" * 100001
        with pytest.raises(ValueError, match="Input text too long"):
            count_words(long_text)
    
    def test_input_length_at_limit(self):
        """Test that input at exactly 100,000 characters is accepted."""
        text_at_limit = "a" * 100000
        result = count_words(text_at_limit)
        assert result == {"a" * 100000: 1}
    
    def test_whitespace_only_strings(self):
        """Test that whitespace-only strings return empty dictionary."""
        # Test various whitespace characters
        result = count_words("   ")
        assert result == {}
        
        result = count_words("\t\t\t")
        assert result == {}
        
        result = count_words("\n\n\n")
        assert result == {}
        
        result = count_words("\r\n\r\n")
        assert result == {}
        
        result = count_words(" \t\n\r ")
        assert result == {}
