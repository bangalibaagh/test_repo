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
        """Test that the timestamp is recent (within last few seconds)."""
        timestamp_str = now.get_utc_timestamp()
        timestamp = datetime.datetime.fromisoformat(timestamp_str)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        
        # Should be within 5 seconds
        time_diff = abs((current_time - timestamp).total_seconds())
        assert time_diff < 5, f"Timestamp is not recent enough: {time_diff} seconds difference"
    
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
        
        # Check ISO-8601 format
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+00:00$'
        assert re.match(iso_pattern, output), f"Script output '{output}' is not in valid ISO-8601 format"
        
        # Check it's UTC
        assert output.endswith('+00:00'), f"Script output '{output}' is not in UTC timezone"
    
    def test_multiple_calls_different_timestamps(self):
        """Test that multiple calls return different timestamps."""
        timestamp1 = now.get_utc_timestamp()
        # Small delay to ensure different timestamps
        import time
        time.sleep(0.001)
        timestamp2 = now.get_utc_timestamp()
        
        assert timestamp1 != timestamp2, "Multiple calls should return different timestamps"
