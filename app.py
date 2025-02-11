from flask import Flask, render_template, Response, json, send_file, jsonify
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from consultar_api import consultar_API
from analizador_datos import AnalizadorDeDatos
from reporte_pdf import ReportePDF
from database import ChatbotDB
import os
import zipfile
import logging

app = Flask(__name__)

# Configura rutas para archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(BASE_DIR, "archivocsv/palabras.csv")
RUTA_ANALISIS = os.path.join(BASE_DIR, "archivocsv/palabras_analisis.csv")
RUTA_AUDIOS = os.path.join(BASE_DIR, "archivocsv/audios")
RUTA_AUDIOS_RESPUESTAS = os.path.join(BASE_DIR, "archivocsv/audios_respuestas")
RUTA_GRAFICO1 = os.path.join(BASE_DIR, "static/images/frecuencia_palabras.png")
RUTA_GRAFICO2 = os.path.join(BASE_DIR, "static/images/clasificaciones_palabras.png")
RUTA_PDF = os.path.join(BASE_DIR, "static/reports/reporte_analisis.pdf")
RUTA_ZIP = os.path.join(BASE_DIR, "static/reports/archivos_analisis.zip")

# Inicializa los objetos
speech_to_text = SpeechToText(RUTA_CSV, RUTA_AUDIOS)
tts = TextToSpeech(RUTA_AUDIOS_RESPUESTAS)
analizador = AnalizadorDeDatos(RUTA_CSV)
reporte_pdf = ReportePDF(RUTA_ANALISIS, RUTA_GRAFICO1, RUTA_GRAFICO2, RUTA_PDF)
base = ChatbotDB()

# Ruta para servir la página HTML
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

#Ruta para cargar los chats 
@app.route("/cargar_chats", methods=["GET"])
def cargar_chats():
    try:
        chats = base.obtener_chats()
        if chats:
            return jsonify({"chats": chats})
        else:
            return jsonify({"mensaje": "No hay chats disponibles. Crea un nuevo chat."})
    except Exception as e:
        return jsonify({"error": str(e)})


# Ruta para la interacción con el chatbot
@app.route("/chat", methods=["GET"])
def chat():
    try:
        def generar_respuesta():
            # Capturar audio, transcribir y procesar con OpenAI
            prompt = speech_to_text.escuchar_y_guardar()
            yield f"data: {json.dumps({'texto_transcrito': prompt})}\n\n"
            
            respuesta = consultar_API(prompt)
            yield f"data: {json.dumps({'respuesta': respuesta})}\n\n"
            base.guardar_mensaje(prompt, respuesta)
            
            # Convierte la respuesta a voz (sin bloquear la generación de texto)
            tts.convertir_a_voz(respuesta)
            
            yield "event: end\ndata: {}\n\n"

        # Retornar la respuesta del SSE (Server-Sent Events)
        return Response(generar_respuesta(), content_type='text/event-stream')

    except Exception as e:
        return json.dumps({"error": f"Ocurrió un error: {str(e)}"}), 500
    
#Ruta para detener el audio
@app.route("/detener_audio", methods=["POST"])
def detener_audio():
    tts.detener_audio()
    tts.finalizar()
    return jsonify({'mensaje': 'Audio detenido'})


# Ruta para generar el ZIP
@app.route("/download_report", methods=["GET"])
def download_report():
    try:
        # Generar los gráficos y el PDF
        analizador.analizar_datos()
        reporte_pdf.generar_pdf()

        # Crear el archivo ZIP
        with zipfile.ZipFile(RUTA_ZIP, "w") as zipf:
            zipf.write(RUTA_PDF, arcname="reporte_analisis.pdf")
            zipf.write(RUTA_GRAFICO1, arcname="frecuencia_palabras.png")
            zipf.write(RUTA_GRAFICO2, arcname="clasificaciones_palabras.png")

        # Enviar el archivo ZIP para descarga
        return send_file(RUTA_ZIP, as_attachment=True)
    except Exception as e:
        logging.error(f"Error al generar el archivo ZIP: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    os.makedirs(os.path.dirname(RUTA_CSV), exist_ok=True)
    os.makedirs(RUTA_AUDIOS, exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "static", "reports"), exist_ok=True)
    base.inicializar_base()
    app.run(debug=True)
