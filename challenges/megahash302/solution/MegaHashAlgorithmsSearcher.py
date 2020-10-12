import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../dist'))
from MegaHash import MegaHash

import hashlib
import time
import random
import statistics

class EfficientMegaHashN:
    _single_cycle_dictionary = None
    _collision_len = 2
    _hash_collection = None

    def __init__(self, algorithms, iterations = 1000, iterated_transforms=None):
        if iterations < 2:
            raise Exception("EfficientMegaHashN doesn't work for non-iterated hashing")

        self._iterations = iterations
        self._cycles = []
        self._total_probability = 0

        _collision_target = 'shake_256'

        self._pre_algorithms = []
        self._cycle = algorithms
        self._post_algorithms = []

        while True:
            _nextHash = self._cycle.pop(0)
            self._pre_algorithms.append(_nextHash)
            if _nextHash == _collision_target:
                break
        self._post_algorithms = self._cycle.copy()
        self._cycle.extend(self._pre_algorithms.copy())
    
        print("\tPre-cycle algorithms: " + str(self._pre_algorithms))
        print("\tCycle algorithms:     " + str(self._cycle))
        print("\tPost-cycle aglorithms: " + str(self._post_algorithms))

        self._pre_algorithms = self.hashlib_instantiator(self._pre_algorithms)
        self._cycle = self.hashlib_instantiator(self._cycle)
        self._post_algorithms = self.hashlib_instantiator(self._post_algorithms)

        self._firstAlgorithm = self._pre_algorithms[0].copy()

        #No need to lock, double-initialization is safe, just a waste of time
        if EfficientMegaHashN._single_cycle_dictionary is None:
            _start = time.time()
            print("\tCalculating single transforms...")
            self._single_cycle_dictionary = self.calculate_single_cycle_dictionary()
            print("\tCalculated transforms in " + str(time.time() - _start) + ".")

        if len(EfficientMegaHashN._path_map) == 0:
            _start = time.time()
            print("\tCalculating path map...")
            tmp = self.calculate_cycle_final_map()
            print("\tCalculated path map in " + str(time.time() - _start) + ".")
            _start = time.time()
            self.calculate_cycle_probabilities(tmp)
            self.populate_cycle_lengths(tmp)
            self._path_map = tmp
            print("\tCalculated cycle lengths in " + str(time.time() - _start) + ". Setup complete.")

        if iterated_transforms is None:
            _start = time.time()
            #print("Calculating iterated transforms for " + str(iterations) + "...")
            #self._iterated_dictionary = self.calculate_iterated_dictionary(iterations)
            #print("Calculated iterated transforms in " + str(time.time() - _start) + ". Instantiation complete.")
        else:
            self._iterated_dictionary = iterated_transforms
    
    def partial_hash(self, data, algorithms):
        intermediateHash = data
        for nextAlg in algorithms:
            algorithm = nextAlg.copy()
            algorithm.update(intermediateHash)

            if nextAlg == EfficientMegaHashN._special_case_algorithm:
                intermediateHash = algorithm.digest(EfficientMegaHashN._collision_len)
            else:
                intermediateHash = algorithm.digest()
        return intermediateHash

    _path_map = {}

    def calculate_cycle_final_map(self):
        path_map = {}

        for i in range(0,256**EfficientMegaHashN._collision_len):
            self.build_single_cycle_path(i, path_map)

        return path_map

    def build_single_cycle_path(self, index, path_map):
        tortise = index
        hare = index
        even = False

        path = []
        while hare not in path_map:
            path.insert(0, hare)
            hare = self.advance_iterations(hare)

            if even:
                tortise = self.advance_iterations(tortise)
            even = not even

            if tortise == hare:
                #Cycle detected
                break;

        while len(path) > 0:
            #If search ended with no prior results, we ended on a cycle point
            if hare not in path_map:
                our_point = {"cycle_distance" : 1, 
                             "cycle_entry" : hare}
            #Just increment previous results
            else:
                point = path_map[hare]

                #We are one point further down, at the same cycle entry point
                our_point = {"cycle_distance" : point["cycle_distance"]+1,
                             "cycle_entry" : point["cycle_entry"]}

            addr = path.pop(0)
            path_map[addr] = our_point
            hare = addr
        
        return

    def calculate_single_cycle_dictionary(self):
        cycle_dictionary = {}

        for i in range(0,256**EfficientMegaHashN._collision_len):
            key = i
            hash = int.from_bytes(self.partial_hash(key.to_bytes(EfficientMegaHashN._collision_len, byteorder='big'), self._cycle), byteorder='big')
            cycle_dictionary[key] = hash

        return cycle_dictionary

    def calculate_cycle_probabilities(self, cache):
        cycleInstances = {}

        for idx in range(0,256**EfficientMegaHashN._collision_len):
            point = cache[idx]

            if point["cycle_entry"] in cycleInstances:
                cycleInstances[point["cycle_entry"]] += 1
            else:
                cycleInstances[point["cycle_entry"]] = 1

        self._cycleInstances = cycleInstances

    def populate_cycle_length(self, cache, cyclePoint):
        cycleEntry = cyclePoint["cycle_entry"]
        length = 1
        #print("\t\t" + str(cycleEntry))
        ptr = self.advance_iterations(cycleEntry)
        #Caclulate cycle length
        while ptr != cycleEntry:
            length += 1
            #print("\t\t" + str(ptr))
            ptr = self.advance_iterations(ptr)
            

        #Populate length for all points in cycle
        while True:
            cache[ptr]["cycle_length"] = length
            ptr = self.advance_iterations(ptr)
            if(ptr == cycleEntry):
                break

        self._cycles.append(length)
        print("\tCycle #" + str(len(self._cycles)) + " length " + str(length) + " Entry point " + str(cycleEntry) + ".")

        self._total_probability += (1/length) * (self._cycleInstances[cycleEntry]/(256**EfficientMegaHashN._collision_len))

        print("\t\tCycle probability 1 in " + str(round(1/((self._cycleInstances[cycleEntry] / (256**EfficientMegaHashN._collision_len)) / length))))
        print("\t\tEntry probability " + str(self._cycleInstances[cycleEntry] / (256**EfficientMegaHashN._collision_len)) + "\t entries " + str(self._cycleInstances[cycleEntry]) )
    
    def populate_cycle_lengths(self, cache):
        for idx in range(0,256**EfficientMegaHashN._collision_len):
            point = cache[idx]
            if "cycle_length" not in cache[idx]:
                if "cycle_length" not in cache[point["cycle_entry"]]:
                    self.populate_cycle_length(cache, point)
                point["cycle_length"] = cache[point["cycle_entry"]]["cycle_length"]


    def advance_iterations(self, ptr, iterations = 1):
        while iterations > 0:
            ptr = self._single_cycle_dictionary[ptr]
            iterations -= 1

        return ptr

    def calculate_iterated_dictionary(self, iterations):
        iterated_dictionary = {}
        cycle_distances = {}

        for start in range(0,256**EfficientMegaHashN._collision_len):
            point = self._path_map[start]

            distanceToGo = iterations-1
            if distanceToGo < point["cycle_distance"]:
                end = self.advance_iterations(start, distanceToGo)
            else:
                distanceToGo -= point["cycle_distance"]

                cycleEntry = point["cycle_entry"]

                distanceToGo %= point["cycle_length"]
                end = self.advance_iterations(cycleEntry, distanceToGo)

            iterated_dictionary[start.to_bytes(EfficientMegaHashN._collision_len, byteorder='big')] = end.to_bytes(EfficientMegaHashN._collision_len, byteorder='big')

        return iterated_dictionary

    def single_hash(self, iterations, data):
        start = int.from_bytes(self.partial_hash(data.encode('ASCII'), self._pre_algorithms), byteorder='big')

        point = self._path_map[start]

        distanceToGo = iterations-1
        if distanceToGo < point["cycle_distance"]:
            end = self.advance_iterations(start, distanceToGo)
        else:
            distanceToGo -= point["cycle_distance"]

            cycleEntry = point["cycle_entry"]
            if "cycle_length" not in self._path_map[cycleEntry]:
                self.populate_cycle_length(point)

            distanceToGo %= self._path_map[cycleEntry]["cycle_length"]
            end = self.advance_iterations(cycleEntry, distanceToGo)

        return self.partial_hash(end.to_bytes(EfficientMegaHashN._collision_len, byteorder='big'), self._post_algorithms)


    def hashlib_instantiator(self, list):
        if EfficientMegaHashN._hash_collection is None:
            EfficientMegaHashN._hash_collection = {}

            MegaHashAlgorithms = ['sha3_384', 'blake2s', 'sha3_256', 'sha224', 'sha384', 'md5', 'sha3_224', 'shake_256', 'sha256', 'sha512', 'sha1', 'sha3_512', 'blake2b']

            for name in MegaHashAlgorithms:
                algorithm = hashlib.new(name)
                EfficientMegaHashN._hash_collection[name] = algorithm

                if name == "shake_256":
                    EfficientMegaHashN._special_case_algorithm = algorithm

        return [EfficientMegaHashN._hash_collection[name] for name in list]

    def new():
        return EfficientMegaHashN()

    def update(self, data):
        self._firstAlgorithm.update(data)

    def copy(self):
        newobj = EfficientMegaHashN(iterations=self._iterations, iterated_transforms=self._iterated_dictionary)
        newobj._firstAlgorithm = self._firstAlgorithm.copy()
        return newobj

    def digest(self):
        intermediateHash = self._firstAlgorithm.digest()
        collision = self.partial_hash(intermediateHash, self._pre_algorithms[1:])
        result = self._iterated_dictionary[collision]
        return self.partial_hash(result, self._post_algorithms)

 

emhn = EfficientMegaHashN(['sha3_384', 'blake2s', 'sha3_256', 'sha224', 'sha384', 'md5', 'sha3_224', 'shake_256', 'sha256', 'sha512', 'sha1', 'sha3_512', 'blake2b'])
print("*****Input average cycle length: " + str(statistics.mean(emhn._cycles)) + " Maximum length: " + str(max(emhn._cycles)) + " ******")
print(emhn._total_probability)
print(len(emhn._cycles))
print("Smoothness is 1 in " + str(1/(emhn._total_probability / len(emhn._cycles))))
print("0," + str(statistics.mean(emhn._cycles)) + "," + str(max(emhn._cycles)) + "")

emhn = EfficientMegaHashN(['blake2s', 'sha3_256', 'blake2s', 'md5', 'sha1', 'sha3_224', 'sha512', 'sha3_512', 'shake_256', 'sha224', 'sha256', 'sha384', 'blake2b'])
print("*****Input average cycle length: " + str(statistics.mean(emhn._cycles)) + " Maximum length: " + str(max(emhn._cycles)) + " ******")
print(emhn._total_probability)
print(len(emhn._cycles))
print("Smoothness is 1 in " + str(1/(emhn._total_probability / len(emhn._cycles))))
print("0," + str(statistics.mean(emhn._cycles)) + "," + str(max(emhn._cycles)) + "")
emhn = EfficientMegaHashN(['blake2s', 'md5', 'sha224', 'blake2s', 'sha3_512', 'sha256', 'sha1', 'sha3_224', 'sha3_256', 'sha512', 'shake_256', 'sha384', 'blake2b'])
print("*****Input average cycle length: " + str(statistics.mean(emhn._cycles)) + " Maximum length: " + str(max(emhn._cycles)) + " ******")
print("Smoothness is 1 in " + str(1/(emhn._total_probability / len(emhn._cycles))))
print("0," + str(statistics.mean(emhn._cycles)) + "," + str(max(emhn._cycles)) + "")

MegaHashAlgorithms = ['sha3_384', 'blake2s', 'sha3_256', 'sha224', 'sha384', 'md5', 'sha3_224', 'shake_256', 'sha256', 'sha512', 'sha1', 'sha3_512', 'blake2b']

random.seed(3)

randomizableAlgorithms = ['blake2s', 'sha3_256', 'sha224', 'sha384', 'md5', 'sha3_224', 'shake_256', 'sha256', 'sha512', 'sha1', 'sha3_512']

while True:
    random.shuffle(randomizableAlgorithms)

    testAlgorithms = [MegaHashAlgorithms[1]]
    testAlgorithms += randomizableAlgorithms
    testAlgorithms += [MegaHashAlgorithms[-1]]

    print("\tInput algorithms: " + str(testAlgorithms))
    print()

    emhn = EfficientMegaHashN(testAlgorithms)
    print()
    print("*****Input average cycle length: " + str(statistics.mean(emhn._cycles)) + " Maximum length: " + str(max(emhn._cycles)) + " ******")
    print("Smoothness is 1 in " + str(1/(emhn._total_probability / len(emhn._cycles))))
    print("0," + str(statistics.mean(emhn._cycles)) + "," + str(max(emhn._cycles)) + "," + str(1/(emhn._total_probability / len(emhn._cycles))))
    print()
    print()
