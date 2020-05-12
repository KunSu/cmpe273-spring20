# Reference: https://techspot.zzzeek.org/2012/07/07/the-absolutely-simplest-consistent-hashing-example/

import pickle
import hashlib
import bisect
from server_config import NODES
from node_ring import NodeRing

class ConsistentHashing():
    
    def __init__(self, ring, replication_factor=1):
        self._ring = ring
        self._replica = replication_factor
        self._keys = []
        self._nodes = {}
        self._load_balanced = {}
        self.generate_virtual_ring()
        
        for index in range(len(self._ring)):
            self._load_balanced[index] = 0

    def replica_hashes(self, node):
        hashes = []
        for i in range(1, self._replica + 1):
            replica_hashe = self.get_hash("%s:%s" % (node, i)) 
            hashes.append(replica_hashe)
        return hashes

    def generate_virtual_ring(self):
        
        for node in self._ring:
            hashes = self.replica_hashes(node)   
            for h in hashes:
                h = self.get_hash(h)

                # use bisect to insert into the right position
                bisect.insort(self._keys, h)
                self._nodes[h] = node

    def get_hash(self, node):
        return int(hashlib.md5(pickle.dumps(node)).hexdigest(), 16)

    def get_node(self, key):
        key = self.get_hash(key)

        # use bisect to find the right index
        index = bisect.bisect(self._keys, key)

        # Reset index
        if index == len(self._keys):
            index = 0

        self._load_balanced[index] += 1
        return self._nodes[self._keys[index]]

    def load_balanced(self):
        return self._load_balanced
