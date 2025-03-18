#!/usr/local/bin/python

from Crypto.Util.number import getPrime, bytes_to_long
import math

with open('flag.txt', 'rb') as f:
    flag = f.read().strip()
    pt = bytes_to_long(flag)
    assert pt.bit_length() > 800

def try_gen():
    p = getPrime(512)
    q = getPrime(512)
    e = getPrime(256)
    N = p*q

    phi = (p-1)*(q-1)
    if math.gcd(phi, e) != 1:
        # restart
        try_gen()

    ct = pow(pt, e, N)
    print('ct =', ct)
    print('e =', e)
    for i in [2,3,4,5,6]:
        print(f'{i}^e mod p =', pow(i, e, p))

try_gen()
