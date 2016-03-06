from random import random
from Crypto.Cipher import AES
import md5
import base64

from primes import get_prime

"""
implimentation of diffie-helmann key exchange based on code found http://www.securityfocus.com/blogs/267

"""

def is_primitive_root(n, prime):
    """
    number g is a primitive root modulo n if every number a coprime to n is congruent to a power of g modulo n.
    That is, for every integer a coprime to n, there is an integer k such that gk = a mod n
    this test function checks to see if an integer mod the prime squared to all integers to prime-1
    results in a distinct set, thinking this has to do with being able to encrypt all values with no collisions
    """
    return len(list(set([n**i % prime for i in range(prime-1)]))) == prime-1

def get_primitive_roots(prime):
    return [i for i in range(prime) if is_primitive_root(i, prime)]

def get_primitive_root(prime):
    roots = get_primitive_roots(prime)
    return roots[int(len(roots) * random())]


def generate_diffie_hellman():
    seed = 500
    #both parties agree on a prime and primitive root
    prime = get_prime(seed)
    prim_root = get_primitive_root(prime)

    #a party choose a random number mod prime is their private key
    private_a = int(random() * seed) % prime

    #the prime root raised to the private key mod prime is the public key
    public_A = (prim_root ** private_a) % prime
    private_b = int(random() * seed) % prime
    public_B = (prim_root ** private_b) % prime

    return {
            'prime': prime,
            'prim_root': prim_root,
            'a': private_a,
            'A': public_A,
            'b': private_b,
            'B': public_B
            }


def get_session_keys(dh):
    a = (dh['B'] ** dh['a']) % dh['prime']
    b = (dh['A'] ** dh['b']) % dh['prime']
    assert a == b, '%d, %d calculated session keys are not identical' % (a, b)
    return (int(a), int(b))

def get_keys(dh):
    keys = get_session_keys(dh)
    keyA = md5.new()
    keyA.update(str(keys[0]))
    aesA = "0x" + keyA.digest()
    keyB = md5.new()
    keyB.update(str(keys[1]))
    aesB = "0x" + keyB.digest()
    return (aesA, aesB)

def pad_msg(msg, block_size = 16):
    pad = (block_size - (len(msg) % block_size)) * ' '
    return msg + pad

def test_diffie_helman(dh):
    block_size = 16
    msg = pad_msg(b'Drink your Ovaltine!', block_size)
    keys = get_keys(dh)
    cipherA = AES.new(keys[0][0:16])
    cipherB = AES.new(keys[1][0:16])
    encMsg = cipherA.encrypt(msg)
    print 'Message: ', msg
    print 'Encrypted: ', encMsg
    decMsg = cipherB.decrypt(encMsg)
    print 'Descrypted: ', decMsg
    return msg == decMsg
