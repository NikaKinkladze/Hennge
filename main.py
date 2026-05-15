def is_nonpositive(x):
    return x <= 0

def raise_to_four(x):
    return x ** 4

def validate_range(nums, index):
    if index == len(nums):
        return True
    if nums[index] < -100 or nums[index] > 100:
        return False
    return validate_range(nums, index + 1)

def process(n, results):
    if n == 0:
        return results

    x = int(input())
    nums_str = input().split()

    if not (0 < x <= 100):
        return
    elif len(nums_str) != x:
        results.append(-1)
    else:
        nums = list(map(int, nums_str))

        if not validate_range(nums, 0):
            return
        else:
            filtered = list(filter(is_nonpositive, nums))
            powered = list(map(raise_to_four, filtered))
            results.append(sum(powered))

    return process(n - 1, results)

def main():
    n = int(input())

    if not (1 <= n <= 100):
        return

    results = process(n, [])

    if results is None:
        return

    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    main()