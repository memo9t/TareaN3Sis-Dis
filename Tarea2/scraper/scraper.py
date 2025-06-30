import requests
import time
import pymongo
from datetime import datetime
from metrics.metrics_sender import enviar_metricas_cache
from cache.cache_manager import LRUCache, LFUCache
from cache.traffic_simulator import generate_traffic_keys
import os

# Configuración del área geográfica
LEFT = -70.85
RIGHT = -70.45
BOTTOM = -33.75
TOP = -33.30

BASE_URL = "https://www.waze.com/live-map/api/georss"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.waze.com/es-419/live-map/"
}

# Variables de entorno
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
META = int(os.getenv("META", "10000"))
DELAY = int(os.getenv("DELAY", "5"))

# Conexión a MongoDB
client = pymongo.MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = client["waze"]
collection = db["eventos"]

def obtener_snapshot_georss():
    params = {
        "top": TOP,
        "bottom": BOTTOM,
        "left": LEFT,
        "right": RIGHT,
        "env": "row",
        "types": "alerts,traffic,users"
    }
    try:
        resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
        print("Status code:", resp.status_code)
        if resp.status_code == 200:
            return resp.json()
        else:
            print("Error al pedir datos (código):", resp.status_code)
            return None
    except Exception as e:
        print("Excepción al solicitar datos:", e)
        return None

def recolectar_eventos_georss(cantidad_objetivo=10000, espera_segundos=5):
    eventos_totales = []
    intento = 0
    while len(eventos_totales) < cantidad_objetivo:
        intento += 1
        data = obtener_snapshot_georss()
        if data is None:
            print(f"[Intento {intento}] No se pudo obtener datos, reintentando en {espera_segundos}s…")
            time.sleep(espera_segundos)
            continue

        nuevos = []
        for clave in ("alerts", "traffic", "users"):
            if clave in data and isinstance(data[clave], list):
                nuevos.extend(data[clave])

        print(f"[Intento {intento}] Se obtuvieron {len(nuevos)} eventos nuevos.")
        eventos_totales.extend(nuevos)

        for evento in nuevos:
            evento['timestamp'] = datetime.utcnow()

        if nuevos:
            try:
                collection.insert_many(nuevos)
            except Exception as e:
                print(f"[Mongo] Error al insertar: {e}")

        if len(eventos_totales) >= cantidad_objetivo:
            break

        time.sleep(espera_segundos)

def simular_cache(politica="LRU", cache_size=100, num_keys=1000, num_requests=10000, distrib="zipf"):
    if politica == "LRU":
        cache = LRUCache(cache_size)
    elif politica == "LFU":
        cache = LFUCache(cache_size)
    else:
        raise ValueError("Política de caché no válida")

    traffic = generate_traffic_keys(num_requests, num_keys, distrib)

    for key in traffic:
        if cache.get(key) is None:
            cache.put(key, "valor")

    hits, misses = cache.stats()
    hit_rate = hits / (hits + misses)
    print(f"[Simulación] Política: {politica}, Distrib: {distrib}, Hits: {hits}, Misses: {misses}, Hit Rate: {hit_rate:.2f}")
    return politica, distrib, cache_size, hits, misses, hit_rate

if __name__ == "__main__":
    print(f"Iniciando recolección de {META} eventos (alerts+traffic+users)…\n")
    inicio = datetime.utcnow()
    recolectar_eventos_georss(cantidad_objetivo=META, espera_segundos=DELAY)
    fin = datetime.utcnow()
    duracion = (fin - inicio).total_seconds()
    print(f"\n¡Listo! Datos almacenados en MongoDB.\n")

    # Enviar métrica básica de scraping
    enviar_metricas_cache(
        modulo="scraper",
        politica="N/A",
        distribucion="N/A",
        cache_size=0,
        hits=META,
        misses=0
    )
    print(f"[Elasticsearch] Métrica enviada con {META} eventos y duración de {duracion:.2f} s.")

    # Simulaciones de cache
if __name__ == "__main__":
    print(f"Iniciando recolección de {META} eventos (alerts+traffic+users)…\n")
    inicio = datetime.utcnow()
    recolectar_eventos_georss(cantidad_objetivo=META, espera_segundos=DELAY)
    fin = datetime.utcnow()
    duracion = (fin - inicio).total_seconds()
    print(f"\n¡Listo! Datos almacenados en MongoDB.\n")

    # Enviar métrica básica de scraping
    try:
        enviar_metricas_cache(
            modulo="scraper",
            politica="N/A",
            distribucion="N/A",
            cache_size=0,
            hits=META,
            misses=0
        )
        print(f"[Scraper] Métrica enviada con {META} eventos y duración de {duracion:.2f} s.")
    except Exception as e:
        print(f"[Scraper] Error al enviar métricas a Elasticsearch: {e}")

    # Simulaciones de cache
    print("\nIniciando simulaciones de caché...\n")
    for politica in ["LRU", "LFU"]:
        for distrib in ["uniform", "zipf"]:
            politica, distrib, size, hits, misses, hit_rate = simular_cache(
                politica=politica,
                cache_size=200,
                num_keys=500,
                num_requests=2000,
                distrib=distrib
            )
            print(f"[Scraper] Enviando métricas de simulación ({politica}, {distrib})…")
            try:
                enviar_metricas_cache("scraper", politica, distrib, size, hits, misses)
            except Exception as e:
                print(f"[Scraper] Error enviando métricas de simulación: {e}")

