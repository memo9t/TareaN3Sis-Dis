import numpy as np

def generate_traffic_keys(num_requests: int, num_keys: int, distribution: str):
    if distribution == "zipf":
        a = 2  # parámetro de la ley de Zipf
        raw = np.random.zipf(a, num_requests)
        keys = [f"k{min(x, num_keys)}" for x in raw]
    elif distribution == "uniform":
        keys = [f"k{np.random.randint(1, num_keys+1)}" for _ in range(num_requests)]
    else:
        raise ValueError("Distribución no soportada.")
    return keys
