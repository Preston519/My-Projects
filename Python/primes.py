# Some primality tests

import random

def is_prime(n: int):
    if n <= 1:
        return False
    elif n % 2 == 0:
        return n == 2
    
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def slow_prime(n: int):
    if n <= 1:
        return False
    
    for x in range(2, n):
        if n % x == 0:
            return False
    return True

def fast_prime(n: int):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0 or n % 5 == 0:
        return False
    
    i = 1
    while (6*i + 1) * (6*i + 1) <= n:
        if n % (6*i + 1) == 0:
            return False
        elif (6*i + 5) * (6*i + 5) <= n and n % (6*i + 5) == 0:
            return False
        i += 1
    return True

# There is a small chance of a false positive (but none for false negative). 64 repeat iterations are recommended.
def miller_rabin(n: int):
    r = 0
    d = n-1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    a = random.randint(2, n-2)
    x = pow(a, d, n)
    
    if x == 1 or x == n-1:
        return True
    
    for _ in range(r-1):
        x = pow(x, 2, n)
        if x == n-1:
            return True
    
    return False
    
    


if __name__ == "__main__":
    # import random
    for _ in range(20):
        val = 0
        while val % 2 == 0:
            val = random.randint(0, 1000000000000000000)
        print(val)
        print(fast_prime(val))
        t = is_prime(val)
        print(t)
        # print(slow_prime(val))
        if t:
            input()
        print(all(miller_rabin(val) for _ in range(64)))
    # print(fast_prime(620887648384938410543479072207))
    print(all(miller_rabin(620887648384938410543479072207) for _ in range(64)))