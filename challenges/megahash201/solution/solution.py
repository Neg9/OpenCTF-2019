#!/usr/bin/python3

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../dist'))
from MegaHash import MegaHash

test_vector = MegaHash.hash("Test vector.")
print("Test vector:               " + test_vector.hex())

import hashlib
import time
import itertools, string

collision_len = 2
collision_target = 'shake_256'
exhaustive_search = True

post_collision_algorithms = MegaHash.MegaHashAlgorithms.copy()
while post_collision_algorithms.pop(0) != collision_target:
    pass
print("Post collider list: " + str(post_collision_algorithms))

targetHash = bytes(bytearray.fromhex('990acae7ac30911a57f1cd8ddea7afdd38f4ea31afc2467868f71d6166749c547f3d979a169a2a617c2f2b358c480911d31b1bc763ab63193751e699535a4cfd'))

#Known hash value
knownValues = {
    'test1' : '9b895b5169bfe1460fa91784bc067d580c9429c2c85bc8b1e1cba442d81ae48355dff3f87ed3af4ffa0824c98397926b5850f00e85cd7063a92534a3b29571ac',
    'test2' : 'bca4c843a0018924403c49bc207da8c942e36ccc0f0ad3b4effe97fdcd34f4adaa2f590c3be28b8f91d493f77833dc6e01304bd081a028a5d593584306cefca7' 
}

fastMsg = list(knownValues.keys())[0]
fastHash = bytearray.fromhex(knownValues[fastMsg])
fastMsg = fastMsg.encode('ASCII')

def partial_hash(data, algorithms):
    intermediateHash = data
    for nextAlg in algorithms:
        algorithm = hashlib.new(nextAlg)
        algorithm.update(intermediateHash)
        try:
            intermediateHash = algorithm.digest()
        except TypeError:
            #TODO: Investigate. Runtime error says:
            #   TypeError: Required argument 'length' (pos 1) not found
            intermediateHash = algorithm.digest(collision_len)
    return intermediateHash

def calculate_full_dictionary():
    #new dictionary
    post_collision_dictionary = {}

    for i in range(0,256**collision_len):
        hash = partial_hash(i.to_bytes(collision_len, byteorder='big'), post_collision_algorithms)
        post_collision_dictionary[hash] = i

    return post_collision_dictionary

trans_5C = bytes((x ^ 0x5C) for x in range(256))
trans_36 = bytes((x ^ 0x36) for x in range(256))
blocksize = MegaHash.block_size

def hmac_given_keyhash(keyHash, message):
    outer = MegaHash()
    inner = MegaHash()
    paddedKey = keyHash.ljust(blocksize, b'\0')
    outer.update(paddedKey.translate(trans_5C))
    inner.update(paddedKey.translate(trans_36))
    inner.update(message)
    outer.update(inner.digest())
    return outer.digest()

def checkKey(key):
    for message in knownValues:
        if hmac_given_keyhash(key, message.encode('ASCII')).hex() != knownValues[message]:
            print("Candidate solution failed for known message " + message)
            return False

    return True

verification_vector = partial_hash("Test vector.".encode('ASCII'), MegaHash.MegaHashAlgorithms)
print("Test vector (PartialHash): " + verification_vector.hex())
if test_vector != verification_vector:
    raise Exception("PartialHash did not match test vector")

start = time.time()
print("Start at " + str(start))

full_dict = calculate_full_dictionary()

last = time.time()
print("Full dictionary of output values calculated in " + str(last - start) + ", calculating key that results in message output next.")

if test_vector not in full_dict:
    print("*****Test vector not present in brute force dictionary*****");
else:
    print("Test vector at input " + str(full_dict[test_vector]) +".")

collision = None
for key in full_dict:
    hOut = hmac_given_keyhash(key, fastMsg)
    if(hOut == fastHash):
        print("Found candidate in input " + str(full_dict[key]))
        if not checkKey(key):
            print("Not a valid solution.")
        else:
            if collision != None:
                print("!!!!!!!!!Found duplicate key!!!!!!!")
            print("Found collision with input " + str(full_dict[key]) + " which gives key " + key.hex())
            collision = key
            if not exhaustive_search:
                break

if collision is None:
    print("Did not find any valid keys that allow for all knownValues.")
else:
    print("Collision output key is " + collision.hex() + ". Calculating another password with HMAC key...")

    #Repeat = length of string for brute force
    for inputArray in itertools.product(string.ascii_uppercase, repeat=5):
        input = ''.join(inputArray)
        if(hmac_given_keyhash(collision, input.encode('ASCII')) == targetHash):
            break;

    print("Another password that collides using HMAC key: " + input)
    print("Result: " + hmac_given_keyhash(collision, input.encode('ASCII')).hex())

    print("Second input calculated in " + str(time.time() - last))

print("End at: " + str(time.time()))
print("Elapsed " + str(time.time() - start))