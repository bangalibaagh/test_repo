#!/usr/bin/env python3
"""Tests for the wordcount module."""

import pytest
import sys
import os

# Add the scripts directory to the path so we can import wordcount
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from wordcount import count_words


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
        result = count_words("Hello, world! How are you? I'm fine.")
        expected = {"hello": 1, "world": 1, "how": 1, "are": 1, "you": 1, "i": 1, "m": 1, "fine": 1}
        assert result == expected
    
    def test_mixed_punctuation_and_case(self):
        """Test combination of punctuation and case variations."""
        result = count_words("Hello, Hello! WORLD... world?")
        expected = {"hello": 2, "world": 2}
        assert result == expected
    
    def test_numbers_and_special_chars(self):
        """Test that numbers and special characters are ignored."""
        result = count_words("hello123 world@#$ test 456")
        expected = {"hello": 1, "world": 1, "test": 1}
        assert result == expected
    
    def test_whitespace_variations(self):
        """Test various whitespace characters."""
        result = count_words("hello\tworld\ntest\r\nhello")
        expected = {"hello": 2, "world": 1, "test": 1}
        assert result == expected
    
    def test_only_punctuation(self):
        """Test string with only punctuation returns empty dict."""
        result = count_words("!@#$%^&*()_+-={}[]|\\:;\"'<>?,./")
        assert result == {}
    
    def test_only_numbers(self):
        """Test string with only numbers returns empty dict."""
        result = count_words("123 456 789")
        assert result == {}
    
    def test_mixed_content(self):
        """Test realistic text with mixed content."""
        text = "The quick brown fox jumps over the lazy dog. The dog was really lazy!"
        result = count_words(text)
        expected = {
            "the": 2, "quick": 1, "brown": 1, "fox": 1, "jumps": 1,
            "over": 1, "lazy": 2, "dog": 2, "was": 1, "really": 1
        }
        assert result == expected
