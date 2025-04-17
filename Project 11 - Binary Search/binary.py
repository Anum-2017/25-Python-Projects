import time

def naive_search(l, target):
    """Scan the list from left to right and return index of target."""
    for i in range(len(l)):
        if l[i] == target:
            return i
    return -1

def binary_search(l, target, low=None, high=None):
    """Recursive binary search to find the index of target in a sorted list."""
    if low is None:
        low = 0
    if high is None:
        high = len(l) - 1

    if high < low:
        return -1  # target not found

    midpoint = (low + high) // 2

    if l[midpoint] == target:
        return midpoint
    elif target < l[midpoint]:
        return binary_search(l, target, low, midpoint - 1)
    else:
        return binary_search(l, target, midpoint + 1, high)

def generate_sorted_list():
    return list(range(-30000, 30001))

def main():
    sorted_list = generate_sorted_list()

    print("\n""🐢 Naive Search vs ⚡ Binary Search")
    print("\n""Search for a number between **-30,000 to 30,000** using both methods.")
    
    target = int(input("\n🎯 Enter the number you want to search: "))

    # Naive search
    start_naive = time.time()
    index_naive = naive_search(sorted_list, target)
    end_naive = time.time()
    time_naive = end_naive - start_naive

    # Binary search
    start_binary = time.time()
    index_binary = binary_search(sorted_list, target)
    end_binary = time.time()
    time_binary = end_binary - start_binary

    # Naive search results
    print("\n🐢 Naive Search")
    if index_naive != -1:
        print(f"Found `{target}` at index `{index_naive}`")
    else:
        print("Not found.")
    print(f"⏱️ Time: {time_naive:.6f} seconds")

    # Binary search results
    print("\n⚡ Binary Search")
    if index_binary != -1:
        print(f"Found `{target}` at index `{index_binary}`")
    else:
        print("Not found.")
    print(f"⏱️ Time: {time_binary:.6f} seconds")

if __name__ == '__main__':
    main()
