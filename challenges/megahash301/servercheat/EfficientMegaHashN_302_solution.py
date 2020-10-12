import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from MegaHash import MegaHash

import hashlib
import time

class EfficientMegaHashN:
    _single_cycle_dictionary = None

    def __init__(self, iterations = 1000, iterated_transforms=None):
        if iterations < 2:
            raise Exception("EfficientMegaHashN doesn't work for non-iterated hashing")

        self._iterations = iterations
        self._firstAlgorithm = EfficientMegaHashN._pre_algorithms[0].copy()

        #No need to lock, double-initialization is safe, just a waste of time
        if EfficientMegaHashN._single_cycle_dictionary is None:
            _start = time.time()
            print("Calculating single transforms...")
            EfficientMegaHashN._single_cycle_dictionary = EfficientMegaHashN.calculate_single_cycle_dictionary()
            print("Calculated transforms in " + str(time.time() - _start) + ".")

        if len(EfficientMegaHashN._path_map) == 0:
            _start = time.time()
            print("Calculating path map...")
            tmp = EfficientMegaHashN.calculate_cycle_final_map()
            print("Calculated path map in " + str(time.time() - _start) + ".")
            _start = time.time()
            EfficientMegaHashN.populate_cycle_lengths(tmp)
            EfficientMegaHashN._path_map = tmp
            print("Calculated cycle lengths in " + str(time.time() - _start) + ". Setup complete.")

        if iterated_transforms is None:
            _start = time.time()
            print("Calculating iterated transforms for " + str(iterations) + "...")
            self._iterated_dictionary = EfficientMegaHashN.calculate_iterated_dictionary(iterations)
            print("Calculated iterated transforms in " + str(time.time() - _start) + ". Instantiation complete.")
        else:
            self._iterated_dictionary = iterated_transforms
    
    def partial_hash(data, algorithms):
        intermediateHash = data
        for nextAlg in algorithms:
            algorithm = nextAlg.copy()
            algorithm.update(intermediateHash)
            try:
                intermediateHash = algorithm.digest()
            except TypeError:
                #TODO: Investigate. Runtime error says:
                #   TypeError: Required argument 'length' (pos 1) not found
                intermediateHash = algorithm.digest(EfficientMegaHashN._collision_len)
        return intermediateHash

    _path_map = {}

    def calculate_cycle_final_map():
        path_map = {}

        for i in range(0,256**EfficientMegaHashN._collision_len):
            EfficientMegaHashN.build_single_cycle_path(i, path_map)

        return path_map

    def build_single_cycle_path(index, path_map):
        tortise = index
        hare = index
        even = False

        path = []
        while hare not in path_map:
            path.insert(0, hare)
            hare = EfficientMegaHashN.advance_iterations(hare)

            if even:
                tortise = EfficientMegaHashN.advance_iterations(tortise)
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

    def calculate_single_cycle_dictionary():
        cycle_dictionary = {}

        for i in range(0,256**EfficientMegaHashN._collision_len):
            key = i
            hash = int.from_bytes(EfficientMegaHashN.partial_hash(key.to_bytes(EfficientMegaHashN._collision_len, byteorder='big'), EfficientMegaHashN._cycle), byteorder='big')
            cycle_dictionary[key] = hash

        return cycle_dictionary

    _cycles = []
    def populate_cycle_length(cache, cyclePoint):
        cycleEntry = cyclePoint["cycle_entry"]
        length = 1
        ptr = EfficientMegaHashN.advance_iterations(cycleEntry)
        #Caclulate cycle length
        while ptr != cycleEntry:
            length += 1
            ptr = EfficientMegaHashN.advance_iterations(ptr)

        #Populate length for all points in cycle
        while True:
            cache[ptr]["cycle_length"] = length
            ptr = EfficientMegaHashN.advance_iterations(ptr)
            if(ptr == cycleEntry):
                break

        EfficientMegaHashN._cycles.append(length)
        print("Cycle #" + str(len(EfficientMegaHashN._cycles)) + " length " + str(length))
    
    def populate_cycle_lengths(cache):
        for idx in range(0,256**EfficientMegaHashN._collision_len):
            point = cache[idx]
            if "cycle_length" not in cache[idx]:
                if "cycle_length" not in cache[point["cycle_entry"]]:
                    EfficientMegaHashN.populate_cycle_length(cache, point)
                point["cycle_length"] = cache[point["cycle_entry"]]["cycle_length"]


    def advance_iterations(ptr, iterations = 1):
        while iterations > 0:
            ptr = EfficientMegaHashN._single_cycle_dictionary[ptr]
            iterations -= 1

        return ptr

    def calculate_iterated_dictionary(iterations):
        iterated_dictionary = {}
        cycle_distances = {}

        for start in range(0,256**EfficientMegaHashN._collision_len):
            point = EfficientMegaHashN._path_map[start]

            distanceToGo = iterations-1
            if distanceToGo < point["cycle_distance"]:
                end = EfficientMegaHashN.advance_iterations(start, distanceToGo)
            else:
                distanceToGo -= point["cycle_distance"]

                cycleEntry = point["cycle_entry"]

                distanceToGo %= point["cycle_length"]
                end = EfficientMegaHashN.advance_iterations(cycleEntry, distanceToGo)

            iterated_dictionary[start.to_bytes(EfficientMegaHashN._collision_len, byteorder='big')] = end.to_bytes(EfficientMegaHashN._collision_len, byteorder='big')

        return iterated_dictionary

    def single_hash(iterations, data):
        start = int.from_bytes(EfficientMegaHashN.partial_hash(data.encode('ASCII'), EfficientMegaHashN._pre_algorithms), byteorder='big')

        point = EfficientMegaHashN._path_map[start]

        distanceToGo = iterations-1
        if distanceToGo < point["cycle_distance"]:
            end = EfficientMegaHashN.advance_iterations(start, distanceToGo)
        else:
            distanceToGo -= point["cycle_distance"]

            cycleEntry = point["cycle_entry"]
            if "cycle_length" not in EfficientMegaHashN._path_map[cycleEntry]:
                EfficientMegaHashN.populate_cycle_length(point)

            distanceToGo %= EfficientMegaHashN._path_map[cycleEntry]["cycle_length"]
            end = EfficientMegaHashN.advance_iterations(cycleEntry, distanceToGo)

        return EfficientMegaHashN.partial_hash(end.to_bytes(EfficientMegaHashN._collision_len, byteorder='big'), EfficientMegaHashN._post_algorithms)


    def hashlib_instantiator(list):
        return [hashlib.new(name) for name in list]

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
        collision = EfficientMegaHashN.partial_hash(intermediateHash, EfficientMegaHashN._pre_algorithms[1:])
        result = self._iterated_dictionary[collision]
        return EfficientMegaHashN.partial_hash(result, EfficientMegaHashN._post_algorithms)

    _collision_target = 'shake_256'
    _collision_len = 2

    _pre_algorithms = []
    _cycle = MegaHash.MegaHashAlgorithms.copy()
    _post_algorithms = []

    while True:
        _nextHash = _cycle.pop(0)
        _pre_algorithms.append(_nextHash)
        if _nextHash == _collision_target:
            break
    _post_algorithms = _cycle.copy()
    _cycle.extend(_pre_algorithms.copy())
    
    print("Pre-cycle algorithms: " + str(_pre_algorithms))
    print("Cycle algorithms:     " + str(_cycle))
    print("Post-cycle aglorithms: " + str(_post_algorithms))

    _pre_algorithms = hashlib_instantiator(_pre_algorithms)
    _cycle = hashlib_instantiator(_cycle)
    _post_algorithms = hashlib_instantiator(_post_algorithms)
