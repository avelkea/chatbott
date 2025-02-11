import os
import pandas as pd
import matplotlib.pyplot as plt, matplotlib
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk

# Anti-Grain-Geometry : genera gráficos como imágenes en vez de mostrarlos en una ventana
matplotlib.use('agg')

class AnalizadorDeDatos:
    def __init__(self, ruta_csv):
        self.ruta_csv = os.path.expanduser(ruta_csv)

    def clasificar_palabra(self, palabra):
        """Clasifica una palabra en aguda, grave o esdrújula."""
        tildes = 'áéíóúÁÉÍÓÚ'
        ultima = len(palabra) - 1
        for i, letra in enumerate(palabra):
            if letra in tildes:
                if ultima - i == 0:
                    return 'Aguda'
                elif ultima - i == 1:
                    return 'Grave'
                elif ultima - i >= 2:
                    return 'Esdrújula'
        return 'Aguda' if len(palabra) > 1 and palabra[-1] not in 'nsaeiou' else 'Grave'

    def extraer_palabras_manual(self, texto):
        """Extrae palabras manualmente de un texto."""
        palabras = []
        palabra_actual = ""
        for char in texto:
            if char.isalnum():  # Considerar solo letras y números
                palabra_actual += char
            else:
                if palabra_actual:
                    palabras.append(palabra_actual)
                    palabra_actual = ""
        if palabra_actual:
            palabras.append(palabra_actual)
        return palabras

    def analizar_datos(self):
        """Realiza el análisis de los datos en el archivo CSV y genera gráficos."""
        try:
            # Verificar si el archivo existe
            if not os.path.exists(self.ruta_csv):
                raise FileNotFoundError(f"El archivo {self.ruta_csv} no existe.")

            # Leer el archivo CSV
            df = pd.read_csv(self.ruta_csv)

            # Añadir columnas de análisis
            df['Num_Palabras'] = df['Texto'].str.split().str.len()
            df['Num_Caracteres'] = df['Texto'].str.len()
            df['Contiene_Python'] = df['Texto'].str.contains('Python', case=False, na=False).astype(int)

            # Extraer palabras y clasificarlas
            palabras = []
            clasificaciones = []
            for texto in df['Texto']:
                palabras_texto = self.extraer_palabras_manual(texto)
                palabras.extend(palabras_texto)
                clasificaciones.extend([self.clasificar_palabra(palabra) for palabra in palabras_texto])

            # Crear un nuevo DataFrame para palabras
            df_palabras = pd.DataFrame({'Palabra': palabras, 'Clasificacion': clasificaciones})

            # Calcular métricas
            longitud_promedio = df['Texto'].apply(len).mean()
            frecuencia_palabras = df_palabras['Palabra'].value_counts().head(10)
            clasificacion_frecuencia = df_palabras['Clasificacion'].value_counts()

            # Agregar clasificaciones al DataFrame original
            df['Clasificaciones'] = df['Texto'].apply(lambda texto: [self.clasificar_palabra(palabra) for palabra in self.extraer_palabras_manual(texto)])

            # Guardar el gráfico de frecuencia de palabras clave
            plt.figure(figsize=(10, 6))
            frecuencia_palabras.plot(kind='bar')
            plt.title('Palabras más frecuentes')
            plt.xlabel('Palabras')
            plt.ylabel('Frecuencia')
            plt.xticks(rotation=45)
            plt.tight_layout()
            ruta_palabras = os.path.join("static", "images", "frecuencia_palabras.png")
            plt.savefig(ruta_palabras)
            plt.close()

            # Guardar el gráfico de clasificaciones
            plt.figure(figsize=(8, 5))
            clasificacion_frecuencia.plot(kind='pie', autopct='%1.1f%%')
            plt.title('Distribución de Clasificaciones (Agudas, Graves, Esdrújulas)')
            plt.ylabel('')
            plt.tight_layout()
            ruta_clasificaciones = os.path.join("static", "images", "clasificaciones_palabras.png")
            plt.savefig(ruta_clasificaciones)
            plt.close()

            # Guardar análisis actualizado en un archivo
            ruta_analisis = self.ruta_csv.replace('.csv', '_analisis.csv')
            df.to_csv(ruta_analisis, index=False)

            return {
                "ruta_palabras": ruta_palabras,
                "ruta_clasificaciones": ruta_clasificaciones,
                "longitud_promedio": longitud_promedio
            }

        except Exception as e:
            return {"error": str(e)}
