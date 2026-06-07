#!/usr/bin/env python3
"""Word counting utility.

This module provides functionality to count words in text with case-insensitive
counting and proper punctuation handling.
"""

import re
from typing import Dict


def count_words(text: str) -> Dict[str, int]:
    """Count words in the given text.
    
    Args:
        text: The input text to count words from.
        
    Returns:
        A dictionary mapping each word (lowercase) to its count.
        
    Examples:
        >>> count_words("Hello world")
        {'hello': 1, 'world': 1}
        
        >>> count_words("Hello, Hello! World.")
        {'hello': 2, 'world': 1}
        
        >>> count_words("")
        {}
    """
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
        text = " ".join(sys.argv[1:])
    else:
        text = input("Enter text to count words: ")
    
    result = count_words(text)
    
    if result:
        print("Word counts:")
        for word, count in sorted(result.items()):
            print(f"{word}: {count}")
    else:
        print("No words found.")
