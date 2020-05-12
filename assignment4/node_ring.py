# Reference: https://en.wikipedia.org/wiki/Rendezvous_hashing
# Reference: https://github.com/natashadsouza/Rendezvous-hashing/blob/master/hrw.py

import mmh3
import math
import pickle
import hashlib
from server_config import NODES

# Add Rendezvous (HRW) Hashing into the Node Ring
class NodeRing(object):
    def __init__(self, nodes):
        assert len(nodes) > 0
        self._nodes = nodes

    def add(self, node):
        self._nodes.add(node)

    def nodes(self):
        return self._nodes

    def remove(self, node):
        self._nodes.remove(node)

    # Assign key_i to the node_m where the weight w_im is the largest
    def get_node(self, key):

        key = int(key, 16)
        weights = []
        for node in self._nodes:
            w = weight(node, key)
            weights.append(w)
            print('weight: ', w)

        node_index = weights.index(max(weights))  
        # print('node index: ', node)
        return self._nodes[node_index]

# Compute weight for all nodes
def weight(node, key):
    # 10,000th Prime number
    a = 104729

    # Another Prime number
    b = 73939133

    node_hash = int(hashlib.md5(pickle.dumps(node)).hexdigest(), 16)
    key_hash = int(hashlib.md5(pickle.dumps(key)).hexdigest(), 16)
    weight = (a * ((a * node_hash + b) * key_hash) + b) % (2 ^ 31)

    return weight

def test():
    ring = NodeRing(nodes=NODES)
    node = ring.get_node('9ad5794ec94345c4873c4e591788743a')
    print(node)
    print(ring.get_node('ed9440c442632621b608521b3f2650b8'))


# Uncomment to run the above local test via: python3 node_ring.py
# test()
