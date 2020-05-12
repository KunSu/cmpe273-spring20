# Reference: https://en.wikipedia.org/wiki/Rendezvous_hashing
# Reference: https://github.com/natashadsouza/Rendezvous-hashing/blob/master/hrw.py

import pickle
import hashlib
from server_config import NODES

# Add Rendezvous (HRW) Hashing into the Node Ring
class NodeRing():
    def __init__(self, nodes, seed, weight):
        assert len(nodes) > 0
        self._nodes = nodes

        # load balanced store the workload for each node. 
        # The key is the node index, the value is the number of workload.
        self._load_balanced = {}

        # An array of repersant the seed and weight for each node.
        # defined by user.
        self.seed = seed
        self.weight = weight

        for index in range(len(self._nodes)):
            self._load_balanced[index] = 0

    def load_balanced(self):
        return self._load_balanced

    # Assign key_i to the node_m where the weight w_im is the largest
    def get_node(self, key_hex):

        key = int(key_hex, 16)
        weights = []
        index = 0
        for node in self._nodes:
            w = weight(node, key, self.seed[index], self.weight[index])
            weights.append(w)
            # print('weight: ', self.weight[index])
            index += 1

        node_index = weights.index(max(weights))  
        self._load_balanced[node_index] += 1
        return self._nodes[node_index]

# Compute weight for all nodes
def weight(node, key, seed, weight):
    # The 10,000th Prime number
    a = 104729

    # Another Prime number
    b = 73939133

    node_hash = int(hashlib.md5(pickle.dumps(node)).hexdigest(), 16)
    key_hash = int(hashlib.md5(pickle.dumps(key)).hexdigest(), 16)

    score = ((seed * ((a * node_hash) + b) * key_hash) + b) % (2 ^ 31)

    return score * weight

def test():
    seed = [1,2,3,4]
    weight = [5,5,5,5]
    ring = NodeRing(nodes=NODES, seed=seed, weight=weight)
    node = ring.get_node('9ad5794ec94345c4873c4e591788743a')
    print(node)
    print(ring.get_node('ed9440c442632621b608521b3f2650b8'))

    LB = ring.load_balanced()
    for index in LB:
        print(LB[index])

# Uncomment to run the above local test via: python3 node_ring.py
test()