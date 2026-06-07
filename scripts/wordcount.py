#!/usr/bin/env python3
"""Word counting utility.

This module provides functionality to count words in text with case-insensitive
counting and proper punctuation handling.
"""

import re
from typing import Dict, Union


def count_words(text: Union[str, None]) -> Dict[str, int]:
    """Count words in the given text.
    
    Args:
        text: The input text to count words from.
        
    Returns:
        A dictionary mapping each word (lowercase) to its count.
        
    Raises:
        TypeError: If text is None or not a string.
        
    Examples:
        >>> count_words("Hello world")
        {'hello': 1, 'world': 1}
        
        >>> count_words("Hello, Hello! World.")
        {'hello': 2, 'world': 1}
        
        >>> count_words("")
        {}
    """
    if text is None:
        raise TypeError("Input text cannot be None")
    
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    if not text:
        return {}
    
    # Remove punctuation and convert to lowercase
    # Split on whitespace and non-word characters
    words = re.findall(r'\b\w+\b', text.lower())
    
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    
    return word_count


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Validate command line arguments to prevent injection
        args = sys.argv[1:]
        # Basic validation - ensure all arguments are strings and not excessively long
        for arg in args:
            if not isinstance(arg, str) or len(arg) > 10000:
                print("Error: Invalid command line argument")
                sys.exit(1)
        text = " ".join(args)
    else:
        text = input("Enter text to count words: ")
    
    try:
        result = count_words(text)
        
        if result:
            print("Word counts:")
            for word, count in sorted(result.items()):
                print(f"{word}: {count}")
        else:
            print("No words found.")
    except TypeError as e:
        print(f"Error: {e}")
        sys.exit(1)
