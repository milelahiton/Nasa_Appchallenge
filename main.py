# main.py
from multi_data import obtener_granulo_reciente, descargar_tempo

# Lista de colecciones TEMPO que querés descargar
COLECCIONES = {
    "NO2 (Dióxido de Nitrógeno)": "C2930763263-LARC_CLOUD",
    "O3 (Ozono Total)": "C2930764281-LARC_CLOUD",
    "AI (Índice de Aerosoles)": "C2930764281-LARC_CLOUD"
}

def ejecutar_descargas():
    for nombre, collection_id in COLECCIONES.items():
        print(f"\n=== Procesando {nombre} ===")
        granule = obtener_granulo_reciente(collection_id)
        if granule:
            url, archivo = granule
            descargar_tempo(url, archivo)
        else:
            print(f"No se encontró granule para {nombre}.")

if __name__ == "__main__":
    ejecutar_descargas()
