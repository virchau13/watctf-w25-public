#!/usr/bin/env python3
import math, pwn, sympy as sp
from sympy.ntheory.modular import crt

def get_one():
    r = pwn.remote('localhost', 5000)
    def lines_as_ints():
        for _ in range(7):
            line = r.recvline().decode('utf-8')
            yield int(line.split(' = ')[1])
    ret = list(lines_as_ints())
    r.close()
    return ret

while True:
    print('trying an iteration')
    ct1, e1, *samples1 = get_one()
    ct2, e2, *samples2 = get_one()

    def get_multiple_of_modulus(samples):
        two_e, three_e, four_e, _, six_e = samples
        return math.gcd(two_e*two_e - four_e, two_e*three_e - six_e)

    p1 = get_multiple_of_modulus(samples1)
    p2 = get_multiple_of_modulus(samples2)
    if sp.isprime(p1) and sp.isprime(p2):
        break

undo_e1 = pow(e1, -1, p1-1)
undo_e2 = pow(e2, -1, p2-1)
pt_residue1 = pow(ct1, undo_e1, p1)
pt_residue2 = pow(ct2, undo_e2, p2)

moduli = [p1, p2]
residues = [pt_residue1, pt_residue2]
pt = crt(moduli, residues)[0]
def int_to_bytes(n):
    return n.to_bytes((n.bit_length() + 7)//8, byteorder='big')
print(int_to_bytes(pt))
