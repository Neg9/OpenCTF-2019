#!/usr/bin/python3

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../dist'))
from MegaHash import MegaHash, MegaHashN

from EfficientMegaHashN import EfficientMegaHashN

import time
import itertools, string

iterations = 137524512181194304293529588298177831395700497192993669968579833476008446723441646580986774908679549078699266485231370906952487688393775950155329524205823852350936697992419085329753164823288025004384515204040111372821422995083130378528560377008059097825548320732324529140605877220741168156860734877457646496436  

targetHash = bytearray.fromhex('3680c937898d5ad5819bcff031b3f2c74f39182bc9a98bbd7944fde16a86d3b88f49f6b36c54bc388bd50c7a69ba3eb99ae39d92681101e40aef8194a8623b31')

emhN = EfficientMegaHashN(iterations=iterations)
tmpHasher = emhN.copy()
tmpHasher.update("Test vector.".encode('ASCII'))

def calcHash(master, data):
    if not isinstance(data, bytes):
       data = data.encode('ASCII')
    tmpHash = master.copy()
    tmpHash.update(data)
    value = tmpHash.digest()
    
    return value

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
