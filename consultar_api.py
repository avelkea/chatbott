from openai import OpenAI
import os

# Configura tu cliente de OpenAI con la clave API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

# Lista para almacenar el historial de mensajes
messages = []

def consultar_API(prompt):
    if not prompt or not prompt.strip():  # Validar si el prompt está vacío o solo tiene espacios
        return "Error: El prompt está vacío. Proporcione un texto válido."
    # Generación de imágenes
    if "imagen" in prompt.lower():
        try:
            imagen = client.images.generate(
                model="dall-e-3",
                prompt=f"{prompt}",
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return imagen.data[0].url
        except Exception as e: 
            return f"Ocurrió un error al comunicarse con la API: {e}"
    else:
        try:
            #forma de interactuar con la API
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages + [{"role": "user", "content": prompt}]
            )
            
            respuesta = completion.choices[0].message.content
            messages.append({"role": "assistant", "content": respuesta})
            return respuesta
        
        except Exception as e:
            #Manejo de errores
            return f"Ocurrió un error al comunicarse con la API: {e}"

def crear_nombre_conversacion(texto):
    prompt = f"Genera un título descriptivo con el siguiente texto: {texto}"

    try:
        titulo = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "Eres un asistente que genera títulos descriptivos del texto."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,  
            temperature=0.7  
        )
        
        # retorna el contenido generado
        return titulo.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Ocurrió un error al comunicarse con la API: {e}"

if __name__ == "__main__":
    print(messages)