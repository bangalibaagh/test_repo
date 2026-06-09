#!/usr/bin/env python3
"""Tests for the wordcount module."""

import pytest
from scripts.wordcount import count_words


class TestCountWords:
    """Test cases for the count_words function."""
    
    def test_empty_string(self):
        """Test that empty string returns empty dictionary."""
        result = count_words("")
        assert result == {}
    
    def test_whitespace_only(self):
        """Test that whitespace-only string returns empty dictionary."""
        result = count_words("   \n\t  ")
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
        result = count_words("hello world hello python world hello")
        expected = {"hello": 3, "world": 2, "python": 1}
        assert result == expected
    
    def test_case_insensitivity(self):
        """Test that words are counted case-insensitively."""
        result = count_words("Hello HELLO hello HeLLo")
        assert result == {"hello": 4}
    
    def test_mixed_case_words(self):
        """Test mixed case with different words."""
        result = count_words("Hello World PYTHON python World")
        expected = {"hello": 1, "world": 2, "python": 2}
        assert result == expected
    
    def test_punctuation_removal(self):
        """Test that punctuation is properly removed."""
        result = count_words("hello, world! python? test.")
        expected = {"hello": 1, "world": 1, "python": 1, "test": 1}
        assert result == expected
    
    def test_complex_punctuation(self):
        """Test handling of complex punctuation patterns."""
        result = count_words("hello... world!!! python??? test...")
        expected = {"hello": 1, "world": 1, "python": 1, "test": 1}
        assert result == expected
    
    def test_punctuation_between_words(self):
        """Test punctuation between words."""
        result = count_words("hello-world python_test")
        expected = {"hello": 1, "world": 1, "python": 1, "test": 1}
        assert result == expected
    
    def test_numbers_and_special_chars(self):
        """Test that numbers and special characters are ignored."""
        result = count_words("hello 123 world @#$ python")
        expected = {"hello": 1, "world": 1, "python": 1}
        assert result == expected
    
    def test_mixed_content(self):
        """Test realistic text with mixed content."""
        text = "Hello, World! This is a test. Hello again, world."
        result = count_words(text)
        expected = {
            "hello": 2,
            "world": 2,
            "this": 1,
            "is": 1,
            "a": 1,
            "test": 1,
            "again": 1
        }
        assert result == expected
    
    def test_newlines_and_tabs(self):
        """Test handling of newlines and tabs."""
        text = "hello\nworld\tpython\r\nhello"
        result = count_words(text)
        expected = {"hello": 2, "world": 1, "python": 1}
        assert result == expected
    
    def test_only_punctuation(self):
        """Test string with only punctuation."""
        result = count_words("!@#$%^&*()_+-={}[]|\\:;\"'<>?,./")
        assert result == {}
    
    def test_contractions(self):
        """Test handling of contractions."""
        result = count_words("don't can't won't it's")
        expected = {"don": 1, "t": 3, "can": 1, "won": 1, "it": 1, "s": 1}
        assert result == expected
