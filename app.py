# Esta versión incluyó el formato tipo WhatsApp para los chats de la IA y el mío.
# Ahora tiene un fondo verde claro, burbujas con bordes redondeados más realistas 
# y colores más vivos para diferenciar entre usuario (verde) e IA (gris).

import streamlit as st
from openai import OpenAI
import os, json

# Cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📂 Ruta de la carpeta memoria
MEMORIA_DIR = "memoria"
MEMORIA_FILE = os.path.join(MEMORIA_DIR, "historial.json")

# Crear carpeta memoria si no existe
if not os.path.exists(MEMORIA_DIR):
    os.makedirs(MEMORIA_DIR)

# Cargar historial desde archivo JSON
def cargar_historial():
    if os.path.exists(MEMORIA_FILE):
        with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Guardar historial en archivo JSON
def guardar_historial(historial):
    with open(MEMORIA_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

# Inicializar historial en sesión
if "historial" not in st.session_state:
    st.session_state.historial = cargar_historial()

# --- CSS personalizado para fondo tipo WhatsApp ---
st.markdown(
    """
    <style>
    .main {
        background-color: #ECE5DD;
        background-image: url("https://i.imgur.com/HQ8oQ5W.png");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💬 Alonso Mejía - Chat IA estilo WhatsApp")

# --- Función que maneja el envío ---
def procesar_mensaje():
    user_input = st.session_state.input_box.strip()
    if user_input:
        # Guardar mensaje del usuario
        st.session_state.historial.append({"role": "user", "content": user_input})

        # Llamar al modelo
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.historial
        )
        answer = response.choices[0].message.content

        # Guardar respuesta
        st.session_state.historial.append({"role": "assistant", "content": answer})

        # Guardar en archivo
        guardar_historial(st.session_state.historial)

    # Limpiar input
    st.session_state.input_box = ""

# Mostrar historial como burbujas estilo WhatsApp
for msg in st.session_state.historial:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="text-align: right;">
                <div style="
                    display: inline-block;
                    background-color: #25D366;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 15px 0px 15px 15px;
                    margin: 5px 0;
                    max-width: 70%;
                    word-wrap: break-word;
                ">
                    {msg['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="text-align: left;">
                <div style="
                    display: inline-block;
                    background-color: #E5E5EA;
                    color: black;
                    padding: 10px 15px;
                    border-radius: 0px 15px 15px 15px;
                    margin: 5px 0;
                    max-width: 70%;
                    word-wrap: break-word;
                ">
                    {msg['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Input al final con Enter para enviar
st.text_input(
    "✏️ Escribe tu mensaje aquí:",
    key="input_box",
    on_change=procesar_mensaje
)

# --- Botón para borrar la memoria ---
if st.button("🧹 Borrar memoria"):
    # Vaciar historial en sesión
    st.session_state.historial = []
    # Eliminar archivo si existe
    if os.path.exists(MEMORIA_FILE):
        os.remove(MEMORIA_FILE)
    st.success("✅ Memoria borrada")
    st.rerun()  # Recargar la app para mostrar vacío
