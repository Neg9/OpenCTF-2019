#!/usr/bin/python3

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../dist'))
from MegaHash import MegaHash

import hashlib
import time
import itertools, string

print(hashlib.algorithms_available)
print(sys.version)

targetHash = bytearray.fromhex('6d64392c0c148bb762667c24afcd516a16aa6a05314a0026ad7dd2be29a1dee906780bb2c38fab0350f24dbd5feb5489093e698b578319a0beac3dbcb398efa2')

print("Start at: " + str(time.time()))
start = time.time()

#Repeat = length of string for brute force
for inputArray in itertools.product(string.ascii_uppercase, repeat=5):
    input = ''.join(inputArray)
    if(MegaHash.hash(input.encode('ASCII')) == targetHash):
        break;

#Oh Python scopes, you so crazy....
print("Colliding string: " + input)
print("End at: " + str(time.time()))
print("Elapsed " + str(time.time() - start) + " seconds.")
