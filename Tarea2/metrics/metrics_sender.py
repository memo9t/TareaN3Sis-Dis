# metrics/metrics_sender.py

from elasticsearch import Elasticsearch
from datetime import datetime

ES_HOST = "http://elasticsearch:9200" 
es = Elasticsearch(
    ES_HOST,
    headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8", 
             "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8"}
)

def enviar_metricas_cache(modulo, politica, distribucion, cache_size, hits, misses):
    hit_rate = hits / (hits + misses)
    doc = {
        "timestamp": datetime.utcnow().isoformat(),
        "modulo": modulo,
        "politica": politica,
        "distribucion": distribucion,
        "cache_size": cache_size,
        "hits": hits,
        "misses": misses,
        "hit_rate": round(hit_rate, 3)
    }
    try:
        print(f"[Elasticsearch] Intentando enviar: {doc}")
        es.index(index="metricas_cache", 
        document=doc ,
        pipeline="pipeline_passthrough"
        )
        print(f"[Elasticsearch] Métrica enviada desde {modulo}")
    except Exception as e:
        print(f"[Elasticsearch] Error: {e}")

