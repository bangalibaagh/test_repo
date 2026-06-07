#!/usr/bin/env python3
"""Tests for the command-line interface of wordcount module."""

import sys
import os
import subprocess
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

# Get the path to the wordcount script
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'wordcount.py')


class TestWordCountCLI:
    """Test cases for the wordcount command-line interface."""
    
    def test_cli_with_arguments(self):
        """Test CLI with command line arguments."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, "hello", "world"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "hello: 1" in result.stdout
        assert "world: 1" in result.stdout
    
    def test_cli_with_repeated_words(self):
        """Test CLI with repeated words in arguments."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, "hello", "hello", "world"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "hello: 2" in result.stdout
        assert "world: 1" in result.stdout
    
    def test_cli_with_no_words(self):
        """Test CLI with arguments that contain no words."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, "!!!", "@@@"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "No words found." in result.stdout
    
    def test_cli_argument_length_validation(self):
        """Test CLI argument length validation."""
        # Create an argument longer than 100000 characters
        long_arg = "a" * 100001
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, long_arg],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
        assert "Error: Command line argument too long" in result.stdout
    
    def test_cli_empty_arguments(self):
        """Test CLI with empty string arguments."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, "", "hello"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "hello: 1" in result.stdout
    
    def test_cli_interactive_mode(self):
        """Test CLI interactive mode when no arguments are provided."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            input="hello world\n",
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Enter text to count words:" in result.stdout
        assert "hello: 1" in result.stdout
        assert "world: 1" in result.stdout
    
    def test_cli_interactive_mode_no_words(self):
        """Test CLI interactive mode with input containing no words."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            input="!!!\n",
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Enter text to count words:" in result.stdout
        assert "No words found." in result.stdout
    
    def test_cli_interactive_mode_long_input(self):
        """Test CLI interactive mode with input exceeding length limit."""
        long_input = "word " * 20001  # Creates input longer than 100,000 chars
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            input=long_input + "\n",
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
        assert "Enter text to count words:" in result.stdout
        assert "Error: Input text too long" in result.stdout
