#!/usr/bin/env python3
"""Word counting utilities.

This module provides functionality to count word frequencies in text.
"""

import re
from typing import Dict


def count_words(text: str) -> Dict[str, int]:
    """Count the frequency of words in the given text.
    
    Args:
        text: The input text to analyze
        
    Returns:
        A dictionary mapping each word to its frequency count.
        Words are converted to lowercase and punctuation is removed.
        
    Examples:
        >>> count_words("Hello world")
        {'hello': 1, 'world': 1}
        
        >>> count_words("Hello, hello world!")
        {'hello': 2, 'world': 1}
    """
    if not text:
        return {}
    
    # Convert to lowercase and extract words (letters, digits, but filter out standalone underscores)
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter out words that are only underscores or other non-alphanumeric characters
    filtered_words = [word for word in words if re.search(r'[a-zA-Z0-9]', word)]
    
    # Count word frequencies
    word_count = {}
    for word in filtered_words:
        word_count[word] = word_count.get(word, 0) + 1
    
    return word_count


if __name__ == "__main__":
    # Example usage
    sample_text = "Hello world! This is a test. Hello again, world."
    result = count_words(sample_text)
    print(f"Word counts: {result}")