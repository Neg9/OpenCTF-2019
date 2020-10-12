#!/usr/bin/python3

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../dist'))
from MegaHash import MegaHash, MegaHashN

from EfficientMegaHashN import EfficientMegaHashN

import time
import itertools, string

iterations = 10000

targetHash = bytearray.fromhex('9b0cef28257380aa5a1896e0a7192abb720ba879ad5087c6dc2b28a6f37886d4f79932069af9efd570ac60f04bc3731cb36d9e85ec03bf03c65d2b86d07c8102')


def calcHash(master, data):
    if not isinstance(data, bytes):
       data = data.encode('ASCII')
    tmpHash = master.copy()
    tmpHash.update(data)
    return tmpHash.digest()

test_vector = calcHash(MegaHashN(iterations=iterations), "Test vector.")
print("Test vector 10:               " + test_vector.hex())

emhN = EfficientMegaHashN(iterations=iterations)
tmpHasher = emhN.copy()
tmpHasher.update("Test vector.".encode('ASCII'))

verification_vector = tmpHasher.digest()
print("Test vector (PartialHash): " + verification_vector.hex())
if test_vector != verification_vector:
    raise Exception("PartialHash did not match test vector")

print("Start at: " + str(time.time()))
start = time.time()

#Repeat = length of string for brute force
for inputArray in itertools.product(string.ascii_uppercase, repeat=5):
    input = ''.join(inputArray)
    if(calcHash(emhN, input.encode('ASCII')) == targetHash):
        break;

#Oh Python scopes, you so crazy....
print("Colliding string: " + input)
print("End at: " + str(time.time()))
print("Elapsed " + str(time.time() - start) + " seconds.")