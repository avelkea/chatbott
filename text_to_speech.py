import pygame
import os
from gtts import gTTS

class TextToSpeech:
    def __init__(self, ruta_audios_respuestas, lang="es", speed=1.3):
        self.ruta_audios_respuestas = os.path.expanduser(ruta_audios_respuestas)
        self.lang = lang
        self.speed = speed

        # Crear el directorio si no existe
        os.makedirs(self.ruta_audios_respuestas, exist_ok=True)

        # Inicialización
        pygame.mixer.init()

    def convertir_a_voz(self, texto):
        try:
            # Contar los archivos existentes en la carpeta
            count = sum(1 for path in os.listdir(self.ruta_audios_respuestas)
                        if os.path.isfile(os.path.join(self.ruta_audios_respuestas, path))
                        and path.startswith("respuesta_")
                        and path.endswith(".mp3"))

            # Genera el nombre del archivo contable
            nombre_archivo = f"respuesta_{count + 1}.mp3"
            ruta_audio = os.path.join(self.ruta_audios_respuestas, nombre_archivo)

            # Crear el archivo de audio usando gTTS
            tts = gTTS(texto, lang=self.lang, slow=False)
            tts.save(ruta_audio)
            print(f"Audio guardado en: {ruta_audio}")

            if not pygame.mixer.get_init():
                pygame.mixer.init()
                
            # Reproducir el archivo con pygame
            self.reproducir_audio(ruta_audio)

            return ruta_audio
        except Exception as e:
            print(f"Ocurrió un error al generar o reproducir el audio: {e}")
            return None

    def reproducir_audio(self, ruta_audio):
        try:
            if not os.path.exists(ruta_audio):
                print("Error: El archivo de audio no existe.")
                return

            # Inicializa el mixer si no está configurado
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            # Cargar y reproducir el archivo de audio
            pygame.mixer.music.load(ruta_audio)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()

            print("Reproducción iniciada...")
            # evitar un uso excesivo de CPU y permitir que otros procesos se ejecuten.
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            self.finalizar()
        except Exception as e:
            print(f"Ocurrió un error al reproducir el audio: {e}")

    def detener_audio(self):
        try:
            # Verifica si el mixer está inicializado y el audio está reproduciéndose
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                print("Reproducción detenida.")
            else:
                print("No hay audio en reproducción.")
        except Exception as e:
            print(f"Ocurrió un error al detener el audio: {e}")    

    def finalizar(self):
        try:
            # Finalizar el mezclador de pygame
            if pygame.mixer.get_init():
                pygame.mixer.quit()
                print("Mezclador de audio finalizado.")
        except Exception as e:
            print(f"Ocurrió un error al finalizar el mezclador: {e}")
