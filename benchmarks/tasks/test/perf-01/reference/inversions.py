def count_inversions(nums):
    """Return the number of inversions in nums.

    An inversion is a pair of positions i < j where nums[i] > nums[j].
    """
    if not isinstance(nums, list):
        raise TypeError("nums must be a list")

    def sort_count(arr):
        n = len(arr)
        if n <= 1:
            return arr, 0
        mid = n // 2
        left, left_count = sort_count(arr[:mid])
        right, right_count = sort_count(arr[mid:])
        merged = []
        i = j = 0
        count = left_count + right_count
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                count += len(left) - i
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, count

    _, total = sort_count(list(nums))
    return total
