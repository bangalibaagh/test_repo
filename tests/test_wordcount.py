#!/usr/bin/env python3
"""Tests for the wordcount module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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
        """Test handling of contractions."""
        result = count_words("don't can't won't")
        expected = {"don": 1, "t": 3, "can": 1, "won": 1}
        assert result == expected