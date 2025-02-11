import pandas as pd
import os

# Define las rutas de los archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_palabras_csv = os.path.join(BASE_DIR, "archivocsv/palabras.csv")
ruta_analisis_csv = os.path.join(BASE_DIR, "archivocsv/palabras_analisis.csv")

# Limpia palabras.csv
def limpiar_palabras_csv():
    if os.path.exists(ruta_palabras_csv):
        # Cargar el archivo
        df = pd.read_csv(ruta_palabras_csv)
        # Mantener solo las columnas necesarias
        df = df[['Texto', 'Ruta_Audio']]
        # Eliminar duplicados basados en Texto y Ruta_Audio
        df = df.drop_duplicates()
        # Guardar el archivo limpio
        df.to_csv(ruta_palabras_csv, index=False)
        print("Archivo palabras.csv limpiado y guardado.")

# Limpia palabras_analisis.csv
def limpiar_analisis_csv():
    if os.path.exists(ruta_analisis_csv):
        # Cargar el archivo
        df = pd.read_csv(ruta_analisis_csv)
        # Asegúrate de que esté limpio
        df = df.drop_duplicates()
        # Guardar el archivo limpio
        df.to_csv(ruta_analisis_csv, index=False)
        print("Archivo palabras_analisis.csv limpiado y guardado.")

# Ejecutar limpieza
limpiar_palabras_csv()
limpiar_analisis_csv()
