
from fractions import gcd
from random import random
from primes import get_primes

"""
learning implimentation based on explanantion here:
https://en.wikipedia.org/wiki/RSA_(cryptosystem)
http://people.csail.mit.edu/rivest/Rsapaper.pdf
"""
def modular_exponent(b,e,m):
    """
    https://en.wikipedia.org/wiki/Modular_exponentiation
    """
    return pow(b, e, m)


def euler_totient(n):
    """
    euler totient takes an integer and return all the numbers
    from 0...n that are relatively prime to n
    """
    return 0


def jacobi_symbol():
    """
    https://en.wikipedia.org/wiki/Jacobi_symbol#Calculating_the_Jacobi_symbol
    jacombi symbol is a generalization of the legendre symbol (a/n)
    if n is an odd prime the legendre and jacobi symbols are the same
    """
    return


def is_coprime(a, b):
    return True if gcd(a, b) == 1 else False


def relatively_prime_generator(n, a=1, b=1):
    """
    https://www.quora.com/What-are-the-fastest-algorithms-for-generating-coprime-pairs
    generates all relatively prime pairs <= n.  The larger number comes first.
    ?no idea how this works?
    """
    yield (a,b)
    k = 1
    while a*k+b <= n:
        for i in relatively_prime_generator(n, a*k+b, a):
            yield i
        k += 1


def get_coprimes(n):
    """
    a is coprime to b if the gcd is 1
    """
    return [p[1] for p in relatively_prime_generator(n) if p[0] == n]


def get_quadratic_recipr(q, p):
    return (p/q)*(q/p) == pow(-1, ((p-1)/2)*((q-1)/2))


def has_quadratic_residue(a, prime):
    """
    https://en.wikipedia.org/wiki/Quadratic_residue
    """
    coprimes = get_coprimes(a)
    for c in coprimes:
        if pow(c, c, prime) == a % prime:
            return True
    return False



def legendre_symbol(a, prime):
    """
    http://codereview.stackexchange.com/questions/43210/tonelli-shanks-algorithm-implementation-of-prime-modular-square-root
    """
    if pow(a, (prime-1)/2, prime) == prime - 1:
        return -1
    return 1


def get_legendre(a,prime):
    """
    https://en.wikipedia.org/wiki/Legendre_symbol
    legedre symbol takes any integer and a prime and returns:
    0 if int and prime are not relatively prime
    -1 if int is not a quadratic residue mod prime
    1 if int is a quadratic residue mod prime and is not 0
    """
    result = a % prime
    if result == 0:
        return 0
    #this is an attmept to calculate quatic residue
    #however I think i need to test all relative primes of of a
    #if (a ** a) % prime == a % prime:
    if has_quadratic_residue(a, prime):
        return 1
    else:
        return -1


def is_probably_prime(a, prime):
    """
    probable prime test based on code here:
    https://en.wikipedia.org/wiki/Solovay%E2%80%93Strassen_primality_test
    """
    return pow(a,(prime-1)/2, prime) == get_legendre(a,prime) % prime


def generate_rsa():
    primes = get_primes(100)
    primes_count = len(primes)
    p = primes[int(random() * primes_count)]
    q = primes[int(random() * primes_count)]
    print p, q
    n = p * q
    etf = (p-1)*(q-1)
    print etf
    coprimes = get_coprimes(etf)
    print coprimes
    e = coprimes[int(len(coprimes)*random())]

    #d is the modular multiplicative inverse
    #http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
    d = (pow(e, etf-2, etf)*e) % etf
    print e, d

    return {
    'q': q,
    'p': p,
    'n': n,
    'etf':etf,
    'e':e,
    'd':d,
    'public':str(n)+'-'+str(e),
    'private':str(n)+'-'+str(d)
    }
