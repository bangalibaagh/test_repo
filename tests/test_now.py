#!/usr/bin/env python3
"""Tests for the now.py script."""

import datetime
import re
import subprocess
import sys
from pathlib import Path

import pytest

# Add scripts directory to path to import now module
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
        
        # Parse the timestamp and verify it's UTC
        parsed = datetime.datetime.fromisoformat(timestamp)
        assert parsed.tzinfo == datetime.timezone.utc, "Timestamp should be in UTC timezone"
    
    def test_get_utc_timestamp_is_recent(self):
        """Test that the timestamp is recent (within last few seconds)."""
        timestamp = now.get_utc_timestamp()
        parsed = datetime.datetime.fromisoformat(timestamp)
        current = datetime.datetime.now(datetime.timezone.utc)
        
        # Should be within 5 seconds
        time_diff = abs((current - parsed).total_seconds())
        assert time_diff < 5, f"Timestamp should be recent, but difference is {time_diff} seconds"
    
    def test_script_execution(self):
        """Test that the script can be executed and produces valid output."""
        script_path = Path(__file__).parent.parent / "scripts" / "now.py"
        
        # Run the script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Script failed with return code {result.returncode}"
        
        output = result.stdout.strip()
        
        # Verify output format
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+00:00$'
        assert re.match(iso_pattern, output), f"Script output '{output}' is not in valid ISO-8601 format"
        
        # Verify it's a valid datetime
        parsed = datetime.datetime.fromisoformat(output)
        assert parsed.tzinfo == datetime.timezone.utc, "Script output should be in UTC timezone"
    
    def test_main_function(self, capsys):
        """Test the main function prints the timestamp."""
        now.main()
        
        captured = capsys.readouterr()
        output = captured.out.strip()
        
        # Verify output format
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+00:00$'
        assert re.match(iso_pattern, output), f"Main function output '{output}' is not in valid ISO-8601 format"
