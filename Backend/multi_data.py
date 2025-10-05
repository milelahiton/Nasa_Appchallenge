import os
import requests

# Token 
EARTHDATA_TOKEN = os.getenv("EARTHDATA_TOKEN") or "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6Imdlcm1hbi5yb3NzaSIsImV4cCI6MTc2NDc4MzIwNCwiaWF0IjoxNzU5NTk5MjA0LCJpc3MiOiJodHRwczovL3Vycy5lYXJ0aGRhdGEubmFzYS5nb3YiLCJpZGVudGl0eV9wcm92aWRlciI6ImVkbF9vcHMiLCJhY3IiOiJlZGwiLCJhc3N1cmFuY2VfbGV2ZWwiOjN9.nVqSsPI8Rmcx6_u_6pvM51pimYdmZCfgQm2G1Im1Stqhttfqiww1roGKZ6Fyqh7tnqAiafqEvgPQSSEyTW3UXT5zaWduH4n0VzxyBk_0AWRr5wdxo7Y0Ym5mNCpuAQBP_KrgLh9yhPsvd9GT_uBePNDhYnlMKXOXSJOSBXsJN2J2TBEVXzPoxEfndzlnMwZ0yuaSTixW4uWZ3UDODryxncNXzF1keAWZIcXmgx4k432xZEGNgWhicgW69QnjE7SAc-beryt-GD8ShPOh3oP2GCJVRZMNX2CJiAO8POSerN-I3yJWHKKJsRYBOOI0KBglsjYX-WgvQd8KNr-LDrTlNw"


def obtener_granulo_reciente(collection_id):
    """Devuelve la URL y el nombre del granule más reciente de una colección dada."""
    cmr_url = "https://cmr.earthdata.nasa.gov/search/granules.json"
    params = {
        "collection_concept_id": collection_id,
        "page_size": 1,
        "sort_key": "-start_date"
    }

    print(f"Buscando el granule más reciente para {collection_id}...")
    r = requests.get(cmr_url, params=params)
    if r.status_code != 200:
        print(f"Error al consultar CMR ({r.status_code})")
        return None

    data = r.json().get("feed", {}).get("entry", [])
    if not data:
        print("No se encontraron granules.")
        return None

    granule = data[0]
    title = granule.get("title")
    links = granule.get("links", [])
    download_url = None

    for link in links:
        if link.get("href", "").endswith(".nc"):
            download_url = link["href"]
            break

    if not download_url:
        print("No se encontró URL .nc.")
        return None

    print(f"Granule más reciente: {title}")
    print(f"URL: {download_url}")
    return download_url, title


def descargar_tempo(url, destino):
    """Descarga un archivo .nc autenticado con Earthdata."""
    if not EARTHDATA_TOKEN:
        print("Falta el token de Earthdata.")
        return

    headers = {"Authorization": f"Bearer {EARTHDATA_TOKEN}"}
    print(f"Descargando archivo desde: {url}")

    try:
        with requests.get(url, headers=headers, stream=True, timeout=600) as r:
            if r.status_code == 200:
                with open(destino, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Descarga completa: {destino}")
            else:
                print(f"Error HTTP {r.status_code}")
                print(r.text[:200])
    except Exception as e:
        print(f"Error durante la descarga: {e}")
