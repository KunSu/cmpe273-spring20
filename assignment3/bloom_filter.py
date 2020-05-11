# Reference: https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
import mmh3
import math
from bitarray import bitarray

class BloomFilter(object): 
  
    ''' 
    n : int
        The number of keys
    p : float 
        The false positive probability
    '''
  
    def __init__(self, n, p): 

        # m is the size of the bit array
        m = - int((n * math.log(p))/(math.log(2)**2)) 

        # hash count is the hash function count
        hash_count = int((m/n) * math.log(2)) 

        self.p = p 
        self.size = m
        self.hash_count = hash_count
  
        # init the bit array
        self.bit_array = bitarray(m) 
        self.bit_array.setall(0) 
  
    # Add element into Bloom Filter
    def add(self, element): 

        for i in range(self.hash_count): 
            block = mmh3.hash(element, i) % self.size 
  
            # set the bit True in bit_array 
            self.bit_array[block] = True
  
    # Check if the element is in the Bloom Filter or not
    def is_member(self, element): 

        for i in range(self.hash_count): 
            block = mmh3.hash(element, i) % self.size 
            if self.bit_array[block] == False: 
                return False
        return True

    # What are the best k hashes and m bits values to store one million n keys (E.g. e52f43cd2c23bb2e6296153748382764) 
    # suppose we use the same MD5 hash key from pickle_hash.py and explain why?
    # The best K should be around 10 and best m should be around 70,000.
    # Having K more than 10, it will start slow down the bloom filter. 
    # If we have fewer k than 10, we may suffer too many false positives.
