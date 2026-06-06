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
        result = count_words("Hello HELLO hello HeLLo")
        assert result == {"hello": 4}
    
    def test_punctuation_handling(self):
        """Test that punctuation is properly stripped."""
        result = count_words("Hello, world! How are you?")
        expected = {"hello": 1, "world": 1, "how": 1, "are": 1, "you": 1}
        assert result == expected
    
    def test_complex_punctuation(self):
        """Test handling of complex punctuation scenarios."""
        result = count_words("Don't worry, it's okay... Really!")
        expected = {"don": 1, "t": 1, "worry": 1, "it": 1, "s": 1, "okay": 1, "really": 1}
        assert result == expected
    
    def test_numbers_and_alphanumeric(self):
        """Test handling of numbers and alphanumeric strings."""
        result = count_words("Python3 is great! Version 3.9 rocks.")
        expected = {"python3": 1, "is": 1, "great": 1, "version": 1, "3": 1, "9": 1, "rocks": 1}
        assert result == expected
    
    def test_whitespace_variations(self):
        """Test handling of various whitespace characters."""
        result = count_words("hello\tworld\nhow\r\nare   you")
        expected = {"hello": 1, "world": 1, "how": 1, "are": 1, "you": 1}
        assert result == expected
    
    def test_only_punctuation(self):
        """Test string with only punctuation returns empty dict."""
        result = count_words("!@#$%^&*()")
        assert result == {}
    
    def test_only_whitespace(self):
        """Test string with only whitespace returns empty dict."""
        result = count_words("   \t\n\r   ")
        assert result == {}


def test_main_function():
    """Test the main function behavior when module is run directly."""
    # This test follows the pattern from test_now.py
    # Testing that the function exists and can be imported
    from scripts.wordcount import count_words
    assert callable(count_words)
    
    # Basic functionality test
    result = count_words("test function")
    assert isinstance(result, dict)
    assert result == {"test": 1, "function": 1}
