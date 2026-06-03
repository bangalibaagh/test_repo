#!/usr/bin/env python3
"""A simple greeting module."""


def greet(name: str) -> str:
    """Return a greeting for the given name.
    
    Args:
        name: The name to greet
        
    Returns:
        A greeting string
        
    Examples:
        >>> greet("Alice")
        'Hello, Alice!'
        >>> greet("Bob")
        'Hello, Bob!'
    """
    if not name:
        return "Hello, there!"
    return f"Hello, {name}!"


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(greet(sys.argv[1]))
    else:
        print(greet(""))
