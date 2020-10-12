#!/usr/bin/python3

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../dist'))
from MegaHash import MegaHash

import hashlib
import time
import itertools, string

print("Start at: " + str(time.time()))
start = time.time()

collision_dictionary = {}

#Repeat = length of string for brute force
for inputArray in itertools.product(string.ascii_uppercase, repeat=5):
    input = ''.join(inputArray)
    hash = MegaHash.hash(input.encode('ASCII'))
    if hash in collision_dictionary:
        print("Collision found with inputs " + input + " and " + collision_dictionary[hash] + ".\nThis gives hash " + hash.hex() + " after " + str(len(collision_dictionary)) + " attempts.")
        
        break
    else:
        collision_dictionary[hash] = input

print("End at: " + str(time.time()))
print("Elapsed " + str(time.time() - start) + " seconds.")
