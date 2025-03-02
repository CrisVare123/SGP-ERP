import json
import os

def cargar_datos(archivo):
    """Carga los datos desde un archivo JSON."""
    if not os.path.exists(archivo):
        return []
    with open(archivo, "r") as f:
        return json.load(f)

def guardar_datos(archivo, datos):
    """Guarda los datos en un archivo JSON."""
    with open(archivo, "w") as f:
        json.dump(datos, f, indent=4)