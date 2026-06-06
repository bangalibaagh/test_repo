#!/usr/bin/env python3
"""Tests for the now.py script."""

import datetime
import re
import subprocess
import sys
from pathlib import Path

import pytest

# Add scripts directory to path for importing
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from now import get_utc_timestamp, main


class TestNowScript:
    """Test cases for the now.py script."""
    
    def test_get_utc_timestamp_format(self):
        """Test that get_utc_timestamp returns a valid ISO-8601 format."""
        timestamp = get_utc_timestamp()
        
        # ISO-8601 format regex pattern
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+00:00$'
        assert re.match(iso_pattern, timestamp), f"Timestamp '{timestamp}' is not in valid ISO-8601 format"
    
    def test_get_utc_timestamp_is_utc(self):
        """Test that the timestamp is in UTC timezone."""
        timestamp = get_utc_timestamp()
        assert timestamp.endswith('+00:00'), "Timestamp should be in UTC timezone (+00:00)"
    
    def test_get_utc_timestamp_is_recent(self):
        """Test that the timestamp is recent (within last few seconds)."""
        timestamp = get_utc_timestamp()
        parsed_time = datetime.datetime.fromisoformat(timestamp)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        
        time_diff = abs((current_time - parsed_time).total_seconds())
        assert time_diff < 5, "Timestamp should be within 5 seconds of current time"
    
    def test_script_execution(self, capsys):
        """Test that the main function prints a timestamp."""
        main()
        captured = capsys.readouterr()
        
        output = captured.out.strip()
        assert output, "Script should produce output"
        
        # Verify it's a valid ISO-8601 timestamp
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+00:00$'
        assert re.match(iso_pattern, output), f"Output '{output}' is not in valid ISO-8601 format"
    
    def test_script_as_executable(self):
        """Test that the script can be executed directly."""
        script_path = Path(__file__).parent.parent / "scripts" / "now.py"
        
        # Run the script as a subprocess
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Script execution failed with return code {result.returncode}"
        
        output = result.stdout.strip()
        assert output, "Script should produce output when executed"
        
        # Verify it's a valid ISO-8601 timestamp
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+00:00$'
        assert re.match(iso_pattern, output), f"Output '{output}' is not in valid ISO-8601 format"
