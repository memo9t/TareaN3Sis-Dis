from collections import OrderedDict, defaultdict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.cache:
            self.hits += 1
            self.cache.move_to_end(key)
            return self.cache[key]
        else:
            self.misses += 1
            return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def stats(self):
        return self.hits, self.misses

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.freq = defaultdict(int)
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.cache:
            self.hits += 1
            self.freq[key] += 1
            return self.cache[key]
        else:
            self.misses += 1
            return None

    def put(self, key, value):
        if key in self.cache:
            self.freq[key] += 1
        else:
            if len(self.cache) >= self.capacity:
                # eliminar el menos usado
                least_freq = min(self.freq.values())
                for k in list(self.cache.keys()):
                    if self.freq[k] == least_freq:
                        del self.cache[k]
                        del self.freq[k]
                        break
            self.freq[key] = 1
        self.cache[key] = value

    def stats(self):
        return self.hits, self.misses
