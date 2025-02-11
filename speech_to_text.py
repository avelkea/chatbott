import speech_recognition as sr
import csv
import os
import pandas as pd

class SpeechToText:
    def __init__(self, ruta_csv, ruta_audios):
        self.ruta_csv = os.path.expanduser(ruta_csv)
        self.ruta_audios = os.path.expanduser(ruta_audios)

        # Crear el directorio para guardar los audios si no existe
        os.makedirs(self.ruta_audios, exist_ok=True)
        print(f"Ruta CSV: {self.ruta_csv}")
        print(f"Ruta audios: {self.ruta_audios}")

        # Crear el archivo CSV con la cabecera si no existe
        if not os.path.exists(self.ruta_csv):
            with open(self.ruta_csv, mode='w', newline='', encoding='utf-8') as archivo_csv:
                escritor = csv.writer(archivo_csv)
                escritor.writerow(["ID", "Texto", "Ruta_Audio"])  # Cabecera del archivo

    def _obtener_ultimo_id(self):
        # Obtiene el último ID del archivo CSV.
        if os.path.exists(self.ruta_csv):
            df = pd.read_csv(self.ruta_csv)
            if not df.empty:
                return df["ID"].max()  # Último ID
        return 0  # Si no hay datos, empieza en 0

    def _guardar_audio(self, audio, id_audio):
        # Guarda el audio en un archivo .wav.
        ruta_audio = os.path.join(self.ruta_audios, f"audio_{id_audio}.wav")
        with open(ruta_audio, "wb") as archivo_audio:
            archivo_audio.write(audio.get_wav_data())
        return ruta_audio

    def escuchar_y_guardar(self):
        try:
            with open(self.ruta_csv, mode='a', newline='', encoding='utf-8') as archivo_csv:
                print("Archivo CSV abierto en modo de agregar.")
                escritor = csv.writer(archivo_csv)

                r = sr.Recognizer()
                r.pause_threshold = 2.0
                r.dynamic_energy_threshold = True
                r.energy_threshold = 150  # Ajusta según el entorno

                # Captura de audio
                with sr.Microphone() as source:
                    
                    print("Di algo:")
                    try:
                        # Se da un tiempo límite de 5 segundos para introducir el input de voz
                        audio = r.listen(source, timeout=5, phrase_time_limit=10)
                        print("Audio capturado.")
                    except Exception as e:
                        print(f"Error al capturar audio: {e}")
                        return None

                # Reconocimiento de texto
                try:
                    # Se usa la API Google Web Speech 
                    text = r.recognize_google(audio, language='es-ES')
                    if not text.strip():
                        raise ValueError("El texto está vacío.")
                    print(f"Texto reconocido: {text}")

                    # Obtener el próximo ID
                    ultimo_id = self._obtener_ultimo_id()
                    nuevo_id = ultimo_id + 1

                    # Guardar el audio y obtener su ruta
                    ruta_audio = self._guardar_audio(audio, nuevo_id)

                    # Escribir el nuevo dato en el archivo CSV
                    escritor.writerow([nuevo_id, text, ruta_audio])
                    print(f"Texto y audio guardados en el archivo CSV con ID {nuevo_id}.")
                    return text
                except sr.UnknownValueError:
                    print("No se pudo reconocer el audio.")
                    return None
                except sr.RequestError as e:
                    print(f"Error con el servicio de reconocimiento: {e}")
                    return None
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None