# Given two large primes p and q, generate an RSA key pair
# If p has m bits and q has n bits, the modulus will have a total of m+n bits

import random

# Returns (modulus, private exponent, public exponent)
# p and q are large primes
def generate_rsa(p: int, q: int, e: int = 65537):
    if not mr_iterate(p):
        raise ValueError("p is not prime")
    elif not mr_iterate(q):
        raise ValueError("q is not prime")
    
    # n is the modulus, as the phi of p*q
    n = (p-1) * (q-1)
    
    gcd, _, d = euclid(n, e)
    if gcd != 1:
        raise ValueError("e is not coprime with modulus")
    
    return (n, d if d > 0 else d+n, e)


def mr_iterate(n: int, k: int = 64):
    return all(miller_rabin(n) for _ in range(64))

# Copied from primes.py
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

def euclid(a: int, b: int):
    if abs(b) > abs(a):
        a, b = b, a
        x0, y0 = 0, 1
        x1, y1 = 1, 0
    else:
        x0, y0 = 1, 0
        x1, y1 = 0, 1
    while b != 0:
        div, mod = divmod(a, b)
        x0, y0, x1, y1 = x1, y1, x0 - div*x1, y0 - div*y1
        a, b = b, mod
    
    if a < 0:
        return (-a, -x0, -y0)
    return (a, x0, y0)

if __name__ == "__main__":
    print(euclid(-240, 50))