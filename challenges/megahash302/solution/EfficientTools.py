import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../dist'))
from MegaHash import MegaHash, MegaHashN

from EfficientMegaHashN import EfficientMegaHashN

import time
import itertools, string

iterations = 137524512181194304293529588298177831395700497192993669968579833476008446723441646580986774908679549078699266485231370906952487688393775950155329524205823852350936697992419085329753164823288025004384515204040111372821422995083130378528560377008059097825548320732324529140605877220741168156860734877457646496436  

emhN = EfficientMegaHashN(iterations=iterations)
tmpHasher = emhN.copy()
tmpHasher.update("Test vector.".encode('ASCII'))

#Used to test new targets for brute force efficiency, for instance for MegaHash301
target = 50126
targetHash = EfficientMegaHashN.partial_hash(target.to_bytes(EfficientMegaHashN._collision_len, byteorder='big'), EfficientMegaHashN._post_algorithms)
print(targetHash.hex())

#Find a given hash in the index
for i in range(0,256**2):
    if targetHash == EfficientMegaHashN.partial_hash(i.to_bytes(EfficientMegaHashN._collision_len, byteorder='big'), EfficientMegaHashN._post_algorithms):
        print("Found hash at index " + str(i))