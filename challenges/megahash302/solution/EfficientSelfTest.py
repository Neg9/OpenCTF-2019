import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../dist'))
from MegaHash import MegaHash, MegaHashN

from EfficientMegaHashN import EfficientMegaHashN

import time
import itertools, string

def calcHash(master, data):
    if not isinstance(data, bytes):
       data = data.encode('ASCII')
    tmpHash = master.copy()
    tmpHash.update(data)
    value = tmpHash.digest()
    
    return value

print("Start at: " + str(time.time()))
start = time.time()

iterations = 2
while iterations < 2**16:
    print("Iterations " + str(iterations))
    hasher = EfficientMegaHashN(iterations=iterations)
    test_vector = calcHash(MegaHashN(iterations=iterations), "Test vector.")
    test_vector_single = EfficientMegaHashN.single_hash(iterations, "Test vector.")
    test_vector_cached = calcHash(hasher, "Test vector.")
    print("Test vector reference:  " + test_vector.hex())
    print("Test vector cached:     " + test_vector_cached.hex())
    print("Test vector single:     " + test_vector_single.hex())
    if test_vector != test_vector_single:
        raise Exception("Single EfficientMegaHash did not match test vector")
    if test_vector != test_vector_cached:
        raise Exception("Cached EfficientMegaHash did not match test vector")
    iterations *= 2

print("Test passed.")
print("End at: " + str(time.time()))
print("Elapsed " + str(time.time() - start) + " seconds.")