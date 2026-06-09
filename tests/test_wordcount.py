#!/usr/bin/env python3
"""Tests for wordcount module."""

import pytest
from scripts.wordcount import count_words


class TestCountWords:
    """Test cases for the count_words function."""
    
    def test_empty_string(self):
        """Test that empty string returns empty dictionary."""
        result = count_words("")
        assert result == {}
    
    def test_single_word(self):
        """Test counting a single word."""
        result = count_words("hello")
        assert result == {"hello": 1}
    
    def test_multiple_words(self):
        """Test counting multiple different words."""
        result = count_words("hello world test")
        expected = {"hello": 1, "world": 1, "test": 1}
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
    
    def test_punctuation_removal(self):
        """Test that punctuation is properly removed."""
        result = count_words("Hello, world! How are you? Fine, thanks.")
        expected = {"hello": 1, "world": 1, "how": 1, "are": 1, "you": 1, "fine": 1, "thanks": 1}
        assert result == expected
    
    def test_numbers_and_special_chars(self):
        """Test handling of numbers and special characters."""
        result = count_words("test123 hello-world @#$% test123")
        expected = {"test123": 2, "hello": 1, "world": 1}
        assert result == expected
    
    def test_whitespace_only(self):
        """Test that whitespace-only string returns empty dictionary."""
        result = count_words("   \n\t  ")
        assert result == {}
    
    def test_punctuation_only(self):
        """Test that punctuation-only string returns empty dictionary."""
        result = count_words("!@#$%^&*()_+-=[]{}|;':,.<>?")
        assert result == {}
    
    def test_mixed_content(self):
        """Test complex text with mixed content."""
        text = "The quick brown fox jumps over the lazy dog. The dog was very lazy!"
        result = count_words(text)
        expected = {
            "the": 3, "quick": 1, "brown": 1, "fox": 1, "jumps": 1,
            "over": 1, "lazy": 2, "dog": 2, "was": 1, "very": 1
        }
        assert result == expected
    
    def test_unicode_characters(self):
        """Test handling of unicode characters."""
        result = count_words("café naïve résumé café")
        expected = {"café": 2, "naïve": 1, "résumé": 1}
        assert result == expected
