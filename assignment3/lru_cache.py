from collections import OrderedDict

# Client-side LRU
class lru_cache(OrderedDict):

    def __init__(self, capacity):
        # init the lru_cache as OrderedDict with  capacity
        self.capacity = capacity

    def __call__(self, f):
        # set the get decorator method
        def get(args):

            str_key = str(args)
            if str_key in self:
                print( '[cache-hit] {}({}) -> {}'.format(f.__name__, str_key, self[str_key]) )
                self.move_to_end(str_key)
                return self[str_key]
            else:

                # put the value into the LRU cache
                value = f(args)
                print( '[cache-not-hit] {}({}) -> {}'.format(f.__name__, str_key, value) )
                self[str_key] = value

                # Remove the last one when exceed LRU capacity
                if len(self) > self.capacity:
                    self.popitem(last = False)
                return value
        return get
