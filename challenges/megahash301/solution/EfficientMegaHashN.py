import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../dist'))
from MegaHash import MegaHash

import hashlib
import time

class EfficientMegaHashN:
    _single_cycle_dictionary = None

    def __init__(self, iterations = 100000, iterated_tranforms=None):
        if iterations < 2:
            raise Exception("EfficientMegaHashN doesn't work for non-iterated hashing")

        self._iterations = iterations
        self._firstAlgorithm = EfficientMegaHashN._pre_algorithms[0].copy()

        #No need to lock, double-initialization is safe, just a waste of time
        if EfficientMegaHashN._single_cycle_dictionary is None:
            _start = time.time()
            print("Calculating single transforms...")
            EfficientMegaHashN._single_cycle_dictionary = EfficientMegaHashN.calculate_single_cycle_dictionary()
            print("Calculated transforms in " + str(time.time() - _start) + ". Setup complete.")

        start = time.time()
        if iterated_tranforms is None:
            print("Calculating iterated transforms for " + str(iterations) + "...")

            self._iterated_dictionary = EfficientMegaHashN.calculate_iterated_dictionary(iterations)

            print("Calculated iterated transforms in " + str(time.time() - start) + ". Instantiation complete.")
        else:
            self._iterated_dictionary = iterated_tranforms
    
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

    def calculate_single_cycle_dictionary():
        cycle_dictionary = {}

        for i in range(0,256**EfficientMegaHashN._collision_len):
            key = i.to_bytes(EfficientMegaHashN._collision_len, byteorder='big')
            hash = EfficientMegaHashN.partial_hash(key, EfficientMegaHashN._cycle)
            cycle_dictionary[key] = hash

        return cycle_dictionary

    def calculate_iterated_dictionary(iterations):
        iterated_dictionary = {}

        for start in range(0,256**EfficientMegaHashN._collision_len):
            end = start.to_bytes(EfficientMegaHashN._collision_len, byteorder='big')
            for i in range(0,iterations-1):
                end = EfficientMegaHashN._single_cycle_dictionary[end]

            iterated_dictionary[start] = end

        return iterated_dictionary

    def hashlib_instantiator(list):
        return [hashlib.new(name) for name in list]

    def new():
        return EfficientMegaHashN()

    def update(self, data):
        self._firstAlgorithm.update(data)

    def copy(self):
        newobj = EfficientMegaHashN(iterations=self._iterations, iterated_tranforms=self._iterated_dictionary)
        newobj._firstAlgorithm = self._firstAlgorithm.copy()
        return newobj

    def digest(self):
        intermediateHash = self._firstAlgorithm.digest()
        collision = int.from_bytes(EfficientMegaHashN.partial_hash(intermediateHash, EfficientMegaHashN._pre_algorithms[1:]), byteorder='big')
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