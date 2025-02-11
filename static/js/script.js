const sendButton = document.getElementById("send-btn");
const chatBox = document.getElementById("chat-box");
const downloadPdfButton = document.getElementById("download-pdf-btn");
const stopButton = document.getElementById("stop-audio-btn");

sendButton.addEventListener("click", async () => {
    // Mostrar mensaje de ajuste al ruido de fondo
    chatBox.innerHTML += `<div class="text-blue-500 font-semibold">Ajustando al ruido de fondo, espera un momento...</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    // Esperar 1 segundo antes de permitir hablar
    setTimeout(() => {
        chatBox.innerHTML += `<div class="text-green-500 font-semibold">Puedes hablar ahora.</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        // Iniciar la conexión con el servidor usando SSE (Server Sent Events)
        const eventSource = new EventSource("/chat");

        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                const messageContainer = document.createElement("div");
                messageContainer.classList.add("message-container", "border", "p-3", "mb-2", "rounded-lg", "shadow")
                if (data.texto_transcrito) {
                    messageContainer.innerHTML += `<div class="font-bold">Tú: ${data.texto_transcrito}</div>`;
                }
                if (data.respuesta) {
                    // Verificar si es una URL de imagen (por ejemplo, empieza con "http" y termina con ".jpg", ".png", etc.)
                    if (data.respuesta.startsWith("http")) {
                        messageContainer.innerHTML += `<div class="font-bold text-red-500">Chatbot:</div>`;
                        messageContainer.innerHTML += `<img src="${data.respuesta}" alt="Imagen generada" class="mt-2 rounded-lg max-w-full h-auto">`;
                    } else {
                        messageContainer.innerHTML += `<div class="font-bold text-red-500">Chatbot: ${data.respuesta}</div>`;
                    }
                }
                //Se agrega el contenedor al chat box
                chatBox.appendChild(messageContainer);
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (error) {
                console.error("Error procesando el mensaje SSE:", error);
            }
        };
        
        eventSource.addEventListener("end", () => {
            eventSource.close();
            chatBox.innerHTML += `<div class="text-blue-500 font-semibold">Presiona de nuevo el boton del micrófono par interactuar.</div>`;
        });
        eventSource.onerror = (error) => {
            console.error("Error en la conexión SSE:", error);
            chatBox.innerHTML += `<div class="text-red-500 font-bold">Error: No se pudo establecer la conexión.</div>`;
            eventSource.close();
        };

        //Cerrar la conexión cuando se complete la conversación

    }, 1000); // Esperar 1 segundo antes de mostrar el mensaje "Puedes hablar ahora"
});

document.getElementById("stop-audio-btn").addEventListener("click", async () => {
    try {
        const response = await fetch("/detener_audio", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.mensaje); // Mensaje recibido del backend
        } else {
            alert(`Error al detener el audio: ${data.mensaje}`);
        }
    } catch (error) {
        alert("Ocurrió un error al intentar detener el audio.");
        console.error("Error:", error);
    }
});

downloadPdfButton.addEventListener("click", async () => {
    try {
        // Llama al endpoint para descargar el ZIP
        const response = await fetch("/download_report", { method: "GET" });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            // Crea un enlace temporal para descargar el archivo
            const a = document.createElement("a");
            a.href = url;
            a.download = "archivos_analisis.zip";
            document.body.appendChild(a);
            a.click();
            a.remove();

            // Libera el objeto URL creado
            window.URL.revokeObjectURL(url);
        } else {
            alert("Error al descargar el reporte.");
        }
    } catch (error) {
        alert("Ocurrió un error al intentar descargar el reporte.");
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.col-lg-3');
    const toggleButton = document.createElement('button');
    toggleButton.textContent = 'Toggle Sidebar';
    toggleButton.classList.add('bg-blue-500', 'text-white', 'p-2', 'rounded', 'lg:hidden');
    document.body.appendChild(toggleButton);

    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('hidden');
    });
    cargarChats();
});

async function cargarChats() {
    try {
        // Hacer la petición GET al backend
        const response = await fetch("/cargar_chats");
        const data = await response.json();

        // Obtener la lista donde se mostrarán los chats
        const listaChats = document.getElementById("lista-chats");

        // Limpiar la lista antes de agregar nuevos elementos
        listaChats.innerHTML = "";

        // Verificar si hay chats disponibles
        if (data.chats && data.chats.length > 0) {
            // Recorrer los chats y agregarlos a la lista
            data.chats.forEach(chat => {
                const listItem = document.createElement("li");
                const link = document.createElement("a");

                link.href = `#`; 
                link.classList.add("text-gray-600", "hover:text-blue-500");
                link.textContent = chat.nombre; 

                listItem.appendChild(link);
                listaChats.appendChild(listItem);
            });
        } else {
            // Mostrar un mensaje si no hay chats
            const mensaje = document.createElement("li");
            mensaje.textContent = "No hay chats disponibles. Crea un nuevo chat.";
            mensaje.classList.add("text-gray-500", "italic");
            listaChats.appendChild(mensaje);
        }
    } catch (error) {
        console.error("Error al cargar los chats:", error);
    }
} 
