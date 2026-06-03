def find_single_number(nums):
    """
    Find the single number that appears exactly once in an array where every other number appears exactly twice.
    
    Args:
        nums: List of integers where all numbers appear twice except one that appears once
        
    Returns:
        int: The number that appears exactly once
        
    Raises:
        ValueError: If the input violates the constraint (multiple numbers appearing once,
                   numbers appearing odd times other than once, etc.)
    """
    if not nums:
        raise ValueError("Input array cannot be empty")
    
    # First, validate that the constraint is satisfied
    # Count occurrences of each number
    count_map = {}
    for num in nums:
        count_map[num] = count_map.get(num, 0) + 1
    
    # Check constraint: exactly one number should appear once, all others should appear even times
    single_count = 0
    for num, count in count_map.items():
        if count % 2 == 1:  # odd count
            if count == 1:
                single_count += 1
            else:
                raise ValueError(f"Number {num} appears {count} times (odd, but not once)")
    
    if single_count == 0:
        raise ValueError("No number appears exactly once")
    elif single_count > 1:
        raise ValueError(f"Multiple numbers ({single_count}) appear exactly once")
    
    # Now apply XOR algorithm since we've validated the constraint
    result = 0
    for num in nums:
        result ^= num
    return result


# Example usage
if __name__ == "__main__":
    # Test case 1: [2, 2, 1]
    nums1 = [2, 2, 1]
    print(f"Input: {nums1}")
    print(f"Single number: {find_single_number(nums1)}")
    
    # Test case 2: [4, 1, 2, 1, 2]
    nums2 = [4, 1, 2, 1, 2]
    print(f"\nInput: {nums2}")
    print(f"Single number: {find_single_number(nums2)}")
    
    # Test case 3: [1]
    nums3 = [1]
    print(f"\nInput: {nums3}")
    print(f"Single number: {find_single_number(nums3)}")
