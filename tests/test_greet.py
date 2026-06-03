#!/usr/bin/env python3
"""Tests for the greet module."""

import pytest
import sys
import os

# Add the scripts directory to the path so we can import greet
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from greet import greet


class TestGreet:
    """Test cases for the greet function."""
    
    def test_greet_with_name(self):
        """Test greeting with a regular name."""
        result = greet("Alice")
        assert result == "Hello, Alice!"
        
    def test_greet_with_different_name(self):
        """Test greeting with another name."""
        result = greet("Bob")
        assert result == "Hello, Bob!"
        
    def test_greet_with_empty_string(self):
        """Test greeting with empty string."""
        result = greet("")
        assert result == "Hello, there!"
        
    def test_greet_with_whitespace_name(self):
        """Test greeting with whitespace in name."""
        result = greet("John Doe")
        assert result == "Hello, John Doe!"
        
    def test_greet_with_special_characters(self):
        """Test greeting with special characters in name."""
        result = greet("José")
        assert result == "Hello, José!"
        
    def test_greet_with_numbers(self):
        """Test greeting with numbers in name."""
        result = greet("User123")
        assert result == "Hello, User123!"
        
    @pytest.mark.parametrize("name,expected", [
        ("Alice", "Hello, Alice!"),
        ("Bob", "Hello, Bob!"),
        ("", "Hello, there!"),
        ("Test User", "Hello, Test User!"),
    ])
    def test_greet_parametrized(self, name, expected):
        """Parametrized test for multiple name inputs."""
        assert greet(name) == expected
