# filtering/filter.py

import pymongo
import csv
import os
from datetime import datetime

MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))

client = pymongo.MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = client["waze"]
collection = db["eventos"]

BASE_DIR = os.path.dirname(__file__)
OUTPUT_CSV = os.path.join(BASE_DIR, "../data/clean_incidents.csv")

def is_valid_doc(doc):
    if 'timestamp' not in doc:
        return False
    tipo = doc.get('type') or doc.get('alertType') or doc.get('subtype')
    if not tipo or not isinstance(tipo, str):
        return False
    loc = doc.get('location') or doc.get('geometry')
    if not loc or not isinstance(loc, dict):
        return False
    lat = loc.get('lat') or loc.get('y')
    lon = loc.get('lon') or loc.get('x')
    if lat is None or lon is None:
        return False
    comuna = doc.get('comuna') or doc.get('city') or doc.get('nearbyStreet')
    if not comuna or not isinstance(comuna, str):
        return False
    return True

def clean_field(value):
    if not isinstance(value, str):
        return ""
   
    return value.replace(",", " ").replace("\n", " ").replace("\r", " ").strip()

def normalize_doc(doc):
    tipo = clean_field((doc.get('type') or doc.get('alertType') or doc.get('subtype')).lower())
    loc = doc.get('location') or doc.get('geometry')
    lat = loc.get('lat') or loc.get('y')
    lon = loc.get('lon') or loc.get('x')
    location_str = f"{float(lat):.6f},{float(lon):.6f}"
    ts_raw = doc.get('timestamp')
    if isinstance(ts_raw, datetime):
        ts = ts_raw.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        try:
            dt = datetime.fromisoformat(ts_raw)
            ts = dt.strftime("%Y-%m-%dT%H:%M:%S")
        except:
            ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    desc = clean_field(doc.get('description') or doc.get('eventDescription') or "")
    comuna_raw = doc.get('comuna') or doc.get('city') or doc.get('nearbyStreet')
    comuna = clean_field(comuna_raw).capitalize()
    return {
        "type": tipo,
        "location": location_str,
        "timestamp": ts,
        "description": desc,
        "comuna": comuna
    }

def exportar_csv_limpio():
    os.makedirs(os.path.join(BASE_DIR, "../data"), exist_ok=True)
    seen_keys = set()

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as fout:
        fieldnames = ["type", "location", "timestamp", "description", "comuna"]
        writer = csv.DictWriter(
            fout,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_MINIMAL,
            escapechar='\\',
            delimiter=','
        )
        writer.writeheader()

        for doc in collection.find():
            if not is_valid_doc(doc):
                continue
            norm = normalize_doc(doc)
            key = (norm["type"], norm["location"], norm["timestamp"])
            if key in seen_keys:
                continue
            writer.writerow(norm)
            seen_keys.add(key)

    print(f"[filter] CSV limpio generado en: {OUTPUT_CSV}")

if __name__ == "__main__":
    exportar_csv_limpio()
