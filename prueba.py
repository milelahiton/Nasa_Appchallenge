import earthaccess
import os
from datetime import datetime, timedelta

print("Iniciando sesión en NASA Earthdata...")

auth = None # Inicia la variable de autenticación
# El script intentará usar credenciales guardadas en .netrc.
# Si falla o no existe, solicitará el ingreso interactivo.
try:
    auth = earthaccess.login(strategy="netrc")
except Exception:
    print("No se encontraron o no funcionaron las credenciales guardadas. Cambiando a modo interactivo...")
    try:
        # Pide al usuario sus credenciales. Esto también creará el archivo .netrc para la próxima vez.
        auth = earthaccess.login(strategy="interactive")
    except Exception as e:
        print(f"El inicio de sesión interactivo falló: {e}")
        exit()

# Verifica si la autenticación fue exitosa antes de continuar
if auth is None or not auth.authenticated:
    print("La autenticación no tuvo éxito. Por favor, verifique sus credenciales. Saliendo.")
    exit()

print("¡Sesión iniciada exitosamente!")

# --- Define el conjunto de datos a buscar basado en tu solicitud ---
# ¡Actualizado! El nombre largo "AIRS/Aqua L3 5-day..." corresponde al short_name "AIRX3Q5D".
datasets_a_buscar = {
    "AIRS_L3_5Day_Quantization": "AIRX3Q5D"
}

# Create a main folder for the downloaded data
if not os.path.exists('datos_worldview'):
    os.makedirs('datos_worldview')

# --- Loop through each dataset, search, and download ---
for nombre_amigable, short_name in datasets_a_buscar.items():
    print(f"\n----------------------------------------------------")
    print(f"Iniciando búsqueda automática de fechas para: {nombre_amigable} ({short_name})")
    
    # --- Bucle para encontrar un período con datos ---
    # Fecha de inicio de la cobertura del producto.
    fecha_actual = datetime.strptime("2002-09-01", "%Y-%m-%d")
    # Límite superior para no buscar indefinidamente.
    fecha_limite = datetime.now()
    # El producto se agrupa en intervalos de 5 días.
    intervalo = timedelta(days=5)
    
    datos_encontrados_y_descargados = False

    while not datos_encontrados_y_descargados and fecha_actual < fecha_limite:
        # Define el rango de 5 días para la búsqueda actual
        fecha_inicio_str = fecha_actual.strftime("%Y-%m-%d")
        fecha_fin_obj = fecha_actual + timedelta(days=4)
        fecha_fin_str = fecha_fin_obj.strftime("%Y-%m-%d")

        print(f"\nIntentando buscar en el rango: {fecha_inicio_str} a {fecha_fin_str}...")
        
        try:
            # Busca los datos para el rango de fechas especificado (globalmente)
            results = earthaccess.search_data(
                short_name=short_name,
                temporal=(fecha_inicio_str, fecha_fin_str),
                count=-1 # Obtiene todos los resultados
            )

            if not results:
                print(f"No se encontraron datos. Probando el siguiente período.")
                # Avanza la fecha al siguiente intervalo de 5 días
                fecha_actual += intervalo
                continue # Salta a la siguiente iteración del bucle while

            # Si llegamos aquí, es porque se encontraron resultados
            print(f"¡Éxito! Se encontraron {len(results)} archivos para este período.")

            # Create a subfolder for this specific dataset
            download_path = os.path.join('datos_worldview', nombre_amigable)
            if not os.path.exists(download_path):
                os.makedirs(download_path)

            # Download the data
            print(f"Iniciando descarga en la carpeta '{download_path}'...")
            earthaccess.download(results, local_path=download_path)
            print(f"Descarga para {nombre_amigable} completada.")
            
            # Marcamos como éxito para salir del bucle while
            datos_encontrados_y_descargados = True

        except Exception as e:
            print(f"Ocurrió un error al procesar el rango {fecha_inicio_str} - {fecha_fin_str}: {e}")
            print("Avanzando al siguiente período para evitar quedar atascado.")
            fecha_actual += intervalo

    if not datos_encontrados_y_descargados:
         print(f"\nNo se encontraron datos para {nombre_amigable} después de buscar hasta la fecha actual.")


print("\n----------------------------------------------------")
print("Proceso finalizado.")