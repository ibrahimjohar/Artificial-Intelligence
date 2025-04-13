#q1

def query(x: int) -> int:
    return -1 * (x-7)**2 + 49

def find_peak(N: int) -> int:
    curr = 0
    while curr < N:
        if query(curr) < query(curr+1):
            curr += 1
        else:
            break
    return curr

print(find_peak(60))
