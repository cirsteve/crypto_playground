from math import sqrt

def is_prime(n):
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_primes(n):
    return [i for i in range(3, n, 2) if is_prime(i)]


def get_prime(limit):
    primes = get_primes(limit)
    return primes[int(len(primes) * random())]
