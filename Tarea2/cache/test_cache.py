from cache_manager import LRUCache, LFUCache
from traffic_simulator import generate_traffic
import time

def evaluate(cache_class, capacity, distribution, iterations=1000, max_key=100):
    cache = cache_class(capacity)
    keys = generate_traffic(distribution, iterations, max_key)

    hits = 0
    misses = 0

    start = time.time()
    for k in keys:
        if cache.get(k) is not None:
            hits += 1
        else:
            cache.put(k, f"value_for_{k}")
            misses += 1
    end = time.time()

    hit_rate = hits / iterations
    print(f"{cache_class.__name__} | {distribution} | Hits: {hits} | Misses: {misses} | Hit rate: {hit_rate:.2f} | Time: {end-start:.3f}s")

# Pruebas
for dist in ["zipf", "uniform", "exponential"]:
    evaluate(LRUCache, 50, dist)
    evaluate(LFUCache, 50, dist)
