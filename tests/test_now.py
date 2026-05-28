#!/usr/bin/env python3
"""Tests for the now.py script."""

import datetime
import re
import subprocess
import sys
from pathlib import Path

import pytest

# Add the scripts directory to the path so we can import now
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

import now


class TestNowScript:
    """Test cases for the now.py script."""
    
    def test_get_utc_timestamp_format(self):
        """Test that get_utc_timestamp returns a valid ISO-8601 format."""
        timestamp = now.get_utc_timestamp()
        
        # ISO-8601 format regex pattern
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+00:00$'
        assert re.match(iso_pattern, timestamp), f"Timestamp '{timestamp}' is not in valid ISO-8601 format"
    
    def test_get_utc_timestamp_is_utc(self):
        """Test that the timestamp is in UTC timezone."""
        timestamp = now.get_utc_timestamp()
        assert timestamp.endswith('+00:00'), f"Timestamp '{timestamp}' is not in UTC timezone"
    
    def test_get_utc_timestamp_is_recent(self):
        """Test that the timestamp is recent (within last minute)."""
        timestamp_str = now.get_utc_timestamp()
        timestamp = datetime.datetime.fromisoformat(timestamp_str)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        
        time_diff = abs((current_time - timestamp).total_seconds())
        assert time_diff < 60, f"Timestamp is not recent enough: {time_diff} seconds ago"
    
    def test_script_execution(self):
        """Test that the script runs successfully and produces valid output."""
        script_path = Path(__file__).parent.parent / "scripts" / "now.py"
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Script failed with return code {result.returncode}"
        assert result.stderr == "", f"Script produced stderr: {result.stderr}"
        
        output = result.stdout.strip()
        
        # Verify output format
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+00:00$'
        assert re.match(iso_pattern, output), f"Script output '{output}' is not in valid ISO-8601 format"
        
        # Verify it's UTC
        assert output.endswith('+00:00'), f"Script output '{output}' is not in UTC timezone"
    
    def test_main_function(self, capsys):
        """Test that the main function prints the timestamp correctly."""
        now.main()
        captured = capsys.readouterr()
        
        output = captured.out.strip()
        
        # Verify output format
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+00:00$'
        assert re.match(iso_pattern, output), f"Main function output '{output}' is not in valid ISO-8601 format"
        
        # Verify it's UTC
        assert output.endswith('+00:00'), f"Main function output '{output}' is not in UTC timezone"
