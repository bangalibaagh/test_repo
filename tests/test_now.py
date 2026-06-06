#!/usr/bin/env python3
"""Tests for the now.py script."""

import datetime
import re
import subprocess
import sys
from pathlib import Path

import pytest

# Add the scripts directory to the path so we can import now
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import now


class TestNowScript:
    """Test cases for the now.py script."""
    
    def test_get_utc_timestamp_format(self):
        """Test that get_utc_timestamp returns a valid ISO-8601 format."""
        timestamp = now.get_utc_timestamp()
        
        # ISO-8601 format regex pattern
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+00:00$"
        
        assert re.match(iso_pattern, timestamp), f"Timestamp '{timestamp}' is not in valid ISO-8601 format"
    
    def test_get_utc_timestamp_microsecond_precision(self):
        """Test that get_utc_timestamp includes microseconds with expected precision."""
        timestamp = now.get_utc_timestamp()
        
        # Extract the microsecond part from the timestamp
        # Format: YYYY-MM-DDTHH:MM:SS.microseconds+00:00
        microsecond_match = re.search(r'\.(\d+)\+00:00$', timestamp)
        
        assert microsecond_match is not None, f"Timestamp '{timestamp}' does not contain microseconds"
        
        microseconds_str = microsecond_match.group(1)
        
        # Verify microseconds are present (non-empty)
        assert len(microseconds_str) > 0, f"Microseconds part is empty in timestamp '{timestamp}'"
        
        # Verify microseconds have expected precision (up to 6 digits for Python datetime)
        assert len(microseconds_str) <= 6, f"Microseconds precision exceeds 6 digits in timestamp '{timestamp}'"
        
        # Verify all characters are digits
        assert microseconds_str.isdigit(), f"Microseconds part contains non-digit characters in timestamp '{timestamp}'"
    
    def test_get_utc_timestamp_is_utc(self):
        """Test that the timestamp is in UTC timezone."""
        timestamp = now.get_utc_timestamp()
        
        # Should end with +00:00 for UTC
        assert timestamp.endswith("+00:00"), f"Timestamp '{timestamp}' is not in UTC timezone"
    
    def test_get_utc_timestamp_is_recent(self):
        """Test that the timestamp is recent (within last few seconds)."""
        timestamp_str = now.get_utc_timestamp()
        timestamp = datetime.datetime.fromisoformat(timestamp_str)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        
        # Should be within 5 seconds of current time
        time_diff = abs((current_time - timestamp).total_seconds())
        assert time_diff < 5, f"Timestamp is not recent enough: {time_diff} seconds difference"
    
    def test_get_utc_timestamp_timezone_aware_parsing(self):
        """Test that the returned timestamp can be parsed back to a timezone-aware datetime object."""
        timestamp_str = now.get_utc_timestamp()
        parsed_datetime = datetime.datetime.fromisoformat(timestamp_str)
        
        # Verify the parsed datetime is timezone-aware
        assert parsed_datetime.tzinfo is not None, f"Parsed datetime from '{timestamp_str}' is not timezone-aware"
        
        # Verify it's in UTC timezone
        assert parsed_datetime.tzinfo == datetime.timezone.utc, f"Parsed datetime timezone is not UTC: {parsed_datetime.tzinfo}"
        
        # Verify we can convert back to the same string representation
        roundtrip_str = parsed_datetime.isoformat()
        assert roundtrip_str == timestamp_str, f"Roundtrip conversion failed: '{timestamp_str}' -> '{roundtrip_str}'"
    
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
        
        # Check that output is valid ISO-8601 format
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+00:00$"
        assert re.match(iso_pattern, output), f"Script output '{output}' is not in valid ISO-8601 format"
    
    def test_main_function(self, capsys):
        """Test that the main function prints a valid timestamp."""
        now.main()
        
        captured = capsys.readouterr()
        output = captured.out.strip()
        
        # Check that output is valid ISO-8601 format
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+00:00$"
        assert re.match(iso_pattern, output), f"Main function output '{output}' is not in valid ISO-8601 format"
