#!/usr/bin/env python3
"""Tests for the now.py script."""

import datetime
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from unittest import mock

import pytest

# Add scripts directory to path for importing
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
        dt = datetime.datetime.fromisoformat(timestamp)
        assert dt.tzinfo == datetime.timezone.utc, "Timestamp should be in UTC timezone"
    
    def test_get_utc_timestamp_is_recent(self):
        """Test that the timestamp is recent (within last few seconds)."""
        timestamp = now.get_utc_timestamp()
        dt = datetime.datetime.fromisoformat(timestamp)
        
        current_time = datetime.datetime.now(datetime.timezone.utc)
        time_diff = abs((current_time - dt).total_seconds())
        
        # Should be within 5 seconds
        assert time_diff < 5, f"Timestamp seems too old or in future: {time_diff} seconds difference"
    
    def test_get_utc_timestamp_ignores_local_timezone(self):
        """Test that the function always returns UTC regardless of local timezone settings."""
        # Mock the TZ environment variable to simulate different system timezone
        with mock.patch.dict(os.environ, {'TZ': 'America/New_York'}):
            # Force timezone reload if available
            if hasattr(time, 'tzset'):
                time.tzset()
            
            timestamp = now.get_utc_timestamp()
            dt = datetime.datetime.fromisoformat(timestamp)
            
            # Verify it's still UTC despite local timezone being set to EST/EDT
            assert dt.tzinfo == datetime.timezone.utc, "Function should return UTC regardless of local timezone"
            
            # Verify the timestamp is still recent (function works correctly)
            current_time = datetime.datetime.now(datetime.timezone.utc)
            time_diff = abs((current_time - dt).total_seconds())
            assert time_diff < 5, "Function should still work correctly with different local timezone"
    
    def test_script_execution(self):
        """Test that the script can be executed and produces valid output."""
        script_path = Path(__file__).parent.parent / "scripts" / "now.py"
