#!/usr/bin/env python3
"""Script that prints the current UTC timestamp in ISO-8601 format."""

import datetime


def get_utc_timestamp() -> str:
    """Get the current UTC timestamp in ISO-8601 format.
    
    Returns:
        str: Current UTC timestamp in ISO-8601 format
    """
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main() -> None:
    """Main function that prints the current UTC timestamp."""
    print(get_utc_timestamp())


if __name__ == "__main__":
    main()
