#!/usr/bin/env python3
"""Word counting utility.

Provides functionality to count word occurrences in text with case-insensitive
matching and proper punctuation handling.
"""

import re
from typing import Dict


def count_words(text: str) -> Dict[str, int]:
    """Count word occurrences in the given text.
    
    Args:
        text: The input text to analyze
        
    Returns:
        A dictionary mapping each word to its occurrence count.
        Words are converted to lowercase and punctuation is stripped.
        
    Examples:
        >>> count_words("Hello world")
        {'hello': 1, 'world': 1}
        >>> count_words("Hello, hello!")
        {'hello': 2}
    """
    if not text:
        return {}
    
    # Convert to lowercase and extract words (alphanumeric sequences)
    words = re.findall(r'\b\w+\b', text.lower())
    
    word_counts: Dict[str, int] = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    return word_counts


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Enter text to count words: ")
    
    counts = count_words(text)
    
    if counts:
        print("Word counts:")
        for word, count in sorted(counts.items()):
            print(f"{word}: {count}")
    else:
        print("No words found.")
