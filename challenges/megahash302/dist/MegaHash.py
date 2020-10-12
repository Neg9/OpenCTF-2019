import hashlib

class MegaHash:
    MegaHashAlgorithms = ['sha3_384', 'blake2s', 'sha3_256', 'sha224', 'sha384', 'md5', 'sha3_224', 'shake_256', 'sha256', 'sha512', 'sha1', 'sha3_512', 'blake2b']

    digest_size = hashlib.new(MegaHashAlgorithms[-1]).digest_size
    block_size = hashlib.new(MegaHashAlgorithms[-1]).block_size
   
    def __init__(self, data = b'', debug = False):
        self._firstAlgorithm = hashlib.new(self.MegaHashAlgorithms[0])
        if debug:
            self._dbgData = [ ]
        else:
            self._dbgData = None
        self.update(data)

    def new():
        return MegaHash()

    def update(self, data):
        if self._dbgData is not None:
            self._dbgData += data
        self._firstAlgorithm.update(data)

    def copy(self):
        newobj = MegaHash()
        newobj.MegaHashAlgorithms = self.MegaHashAlgorithms.copy()
        newobj._firstAlgorithm = self._firstAlgorithm.copy()
        newobj._dbgData = self._dbgData
        return newobj

    def digest(self):
        intermediateHash = self._firstAlgorithm.digest()
        for nextAlg in self.MegaHashAlgorithms[1:]:
            algorithm = hashlib.new(nextAlg)
            algorithm.update(intermediateHash)
            try:
                intermediateHash = algorithm.digest()
            except TypeError:
                #TODO: Investigate. Runtime error says:
                #   TypeError: Required argument 'length' (pos 1) not found
                intermediateHash = algorithm.digest(length = 2)
        if self._dbgData is not None:
            print("Digest for: " + ''.join([bytes([x]).decode('latin1') for x in self._dbgData]) + " ---is--- " + intermediateHash.hex())
        return intermediateHash

    def hash(self, data):
        if not isinstance(data, bytes):
            data = data.encode('ASCII')
        h = self.copy()
        h.update(data)
        return h.digest()

class MegaHashN(MegaHash):
    def __init__(self, data = b'', debug = False, iterations = 1000):
        super().__init__(data=b'', debug=debug)
        self._iterations = iterations
        
        #Duplicate list of algorithms iteration times
        self.MegaHashAlgorithms = self.MegaHashAlgorithms*iterations
        self.update(data)

    def benchmark():
        return 0;