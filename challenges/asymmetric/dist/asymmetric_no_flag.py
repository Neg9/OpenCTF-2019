#!/usr/bin/env python3
"""
RSA + AES
by Javantea
July 23, 2019

"""
import random
import Crypto.Cipher.AES
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse, getPrime

# I never thought of rsa this way before.
def encrypt(msg, k):
    return long_to_bytes(pow(bytes_to_long(msg), k[0], k[1]))

def decrypt(msg, k):
    return long_to_bytes(pow(bytes_to_long(msg), k[0], k[1]))

def verify(msg, k):
    return long_to_bytes(pow(bytes_to_long(msg), k[0], k[1]))

def sign(msg, k):
    return long_to_bytes(pow(bytes_to_long(msg), k[0], k[1]))

def main():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    e = 0x1001
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    # FIXME: 1 in 65536 chance of d being invalid due to e.
    # 128-bit key.
    key = bytes([random.randint(0, 255) for i in range(16)])
    flag = b'flag{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}'
    cipher = Crypto.Cipher.AES
    to_pad = 16 - (len(flag) % cipher.block_size)
    if to_pad == 16: to_pad = 0
    a_pad = flag + (b'\x00' * to_pad)
    ct = encrypt(key, (e, n))
    iv = bytes([random.randint(0, 255) for i in range(16)])
    c = cipher.new(key, mode = cipher.MODE_CBC, iv=iv)
    encrypted = c.encrypt(a_pad)
    se = sign(ct, (d, n))
    c = 1024 >> 3
    c -= len(se)
    sep = bytes([random.randint(0, 255) for i in range(c)])
    se += sep
    print(se)
    print(iv, encrypted)
    print(' '.join(['e = ' + hex(e), 'n = '  + hex(n)]))

if __name__ == '__main__':
    main()
