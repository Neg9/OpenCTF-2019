#!/usr/bin/env python3
"""
RSA + AES
by Javantea
July 23, 2019

"""
import Crypto.Cipher.AES
import reverserepr
import sys

if sys.version_info.major < 3:
    print("This script doesn't support python 2. Like at all.")
    exit(1)

a = open('dist/ciphertext.txt', 'r').read()
b = a.split('\n')

c = reverserepr.reverseRepr(b[0])
print('c', c)
print(c)

iv = reverserepr.reverseRepr(b[1])
q = len(repr(iv))
print(q, b[1])
assert(b[1][q] == ' ')
print('iv', iv)

encrypted = reverserepr.reverseRepr(b[1][q + 1:])
print('enc', encrypted)

key = c[:16]
cipher = Crypto.Cipher.AES

c = cipher.new(key, cipher.MODE_CBC, iv)
decrypted = c.decrypt(encrypted)
print(decrypted)
