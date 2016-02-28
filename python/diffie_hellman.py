from math import sqrt
from random import random
import md5


"""
implimentation of diffie-helmann key exchange based on code found http://www.securityfocus.com/blogs/267

"""
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


def is_primitive_root(n, prime):
    return len(list(set([n**i % prime for i in range(prime-1)]))) == prime-1


def get_primitive_roots(prime):
    return [i for i in range(prime) if is_primitive_root(i, prime)]

def get_primitive_root(prime):
    roots = get_primitive_roots(prime)
    return roots[int(len(roots) * random())]


def generate_diffie_hellman():
    seed = 500
    prime = get_prime(seed)
    prim_root = get_primitive_root(prime)
    private_a = int(random() * seed) % prime
    private_b = int(random() * seed) % prime
    public_A = (prim_root ** private_a) % prime
    public_B = (prim_root ** private_b) % prime
    return {
            'prime': prime,
            'prim_root': prim_root,
            'a': private_a,
            'b':private_b,
            'A': public_A,
            'B': public_B
            }


def get_session_key(dh):
    a = (dh['B'] ** dh['a']) % dh['prime']
    b = (dh['A'] ** dh['b']) % dh['prime']
    assert a == b, '%d, %d calcultad session keys are not identical' % (a, b)
    return int(a)


def get_aes_key(dh):
    key = md5.new()
    key.update(str(get_session_key(dh)))
    return "0x" + key.digest()


