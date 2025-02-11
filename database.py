import sqlite3
import os

class ChatbotDB:
    def __init__(self, db_name="chatbot.db"):
        # Definir la ruta de la base de datos
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
        self.conexion_base()
    
    def conexion_base(self):
        """Establece la conexión con la base de datos."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def inicializar_base(self):
        self.conexion_base()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS conversaciones (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              nombre TEXT NOT NULL)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS mensajes (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              conversacion_id INTEGER NOT NULL,
                              prompt TEXT NOT NULL,
                              respuesta TEXT NOT NULL,
                              FOREIGN KEY (conversacion_id) REFERENCES conversaciones(id) 
                              ON DELETE CASCADE)""")
        self.conn.commit()
        self.close()

    def guardar_conversacion(self, nombre):
        """Guarda una nueva conversación."""
        self.conexion_base()
        self.cursor.execute('INSERT INTO conversaciones (nombre) VALUES (?)', (nombre,))
        self.conn.commit()
        self.close()

    def guardar_mensaje(self, conversacion_id, prompt, respuesta):
        """Guarda un mensaje en una conversación existente."""
        self.conexion_base()
        self.cursor.execute('INSERT INTO mensajes (conversacion_id, prompt, respuesta) VALUES (?, ?, ?)',
                            (conversacion_id, prompt, respuesta))
        self.conn.commit()
        self.close()

    def obtener_mensajes(self, conversacion_id):
        """Obtiene todos los mensajes de una conversación específica."""
        self.conexion_base()
        self.cursor.execute('SELECT prompt, respuesta FROM mensajes WHERE conversacion_id = ?', (conversacion_id,))
        mensajes = self.cursor.fetchall()
        self.close()
        return mensajes

    def obtener_chats(self):
        """Obtiene todos los nombres de las conversaciones."""
        self.conexion_base()
        self.cursor.execute("SELECT COUNT(*) FROM User")
        conteo = self.cursor.fetchone()[0]  # Obtiene el resultado de la consulta
        if conteo > 0:  # Si el conteo es mayor a 0 selecciona los nombres conversaciones
            self.cursor.execute('SELECT nombre FROM conversaciones;')
            nombres = self.cursor.fetchall()
            self.close()
            # Devuelve una lista de strings con los nombres
            # for nombre in nombres : return nombre[0]
            return [nombre[0] for nombre in nombres]
        else: 
            self.close()
            return None
    def crear_nuevo_chat(self, nombre):
        self.conexion_base()
        # Insertar el nuevo chat con el nombre proporcionado
        self.cursor.execute('INSERT INTO conversaciones (nombre) VALUES (?)', (nombre,))
        self.conn.commit()
        conversacion_id = self.cursor.lastrowid
        # Actualizar el nombre del chat con su ID 
        nuevo_nombre = f"{nombre} {conversacion_id}"
        self.cursor.execute('UPDATE conversaciones SET nombre = ? WHERE id = ?', (nuevo_nombre, conversacion_id))
        self.conn.commit()
        self.conn.close()
        