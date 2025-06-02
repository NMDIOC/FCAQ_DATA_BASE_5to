import streamlit as st
import json
import os

# Archivo JSON de la base de datos
DB_FILE = "estudiantes.json"

# Consejos por estilo
consejos = {
    "visual": "Usa mapas mentales, diagramas y colores para enseñar.",
    "auditivo": "Habla en voz alta, usa canciones o rimas.",
    "kinestésico": "Incorpora movimiento, juegos físicos o manualidades.",
    "lector/escritor": "Usa listas, resúmenes y escritura repetida."
}

# Usuarios y contraseñas
usuarios_autorizados = {
    "Nicolas Medina": {"rol": "propietario", "clave": "admin2013"},
    "Tomas Maldonado": {"rol": "admin", "clave": "admin143"},
    "Simon Romoleroux": {"rol": "admin", "clave": "admin153"},
    "Eva Godoy": {"rol": "admin", "clave": "admin3"},
}

# Funciones para la base de datos
def cargar_estudiantes():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_estudiantes(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Función de login
def login():
    st.sidebar.title("🔐 Iniciar sesión")
    usuario = st.sidebar.selectbox("Usuario", ["Seleccionar"] + list(usuarios_autorizados.keys()))
    clave = st.sidebar.text_input("Contraseña", type="password")

    if usuario != "Seleccionar" and clave:
        datos = usuarios_autorizados.get(usuario)
        if datos and clave == datos["clave"]:
            return usuario, datos["rol"]
        else:
            st.sidebar.error("Usuario o contraseña incorrectos")
    return None, None

# Título principal
st.title("🎓 Base de Datos: Estilos de Aprendizaje")

# Cargar estudiantes
estudiantes = cargar_estudiantes()

# Iniciar sesión
usuario, rol = login()

if usuario:
    st.success(f"Bienvenido {usuario} ({rol})")

    # Añadir o editar estudiante
    st.subheader("➕ Añadir o editar estudiante")
    nombre = st.text_input("Nombre del estudiante")
    genero = st.selectbox("Género", ["Masculino", "Femenino"])
    estilo = st.selectbox("Estilo de aprendizaje", list(consejos.keys()))

    if st.button("Guardar estudiante"):
        if nombre:
            estudiantes[nombre] = {"genero": genero, "estilo": estilo}
            guardar_estudiantes(estudiantes)
            st.success(f"{nombre} ha sido guardado con estilo '{estilo}'")
        else:
            st.warning("Por favor, escribí un nombre")

# Búsqueda visible para todos
st.subheader("🔍 Buscar estudiante")
buscar = st.text_input("Buscar por nombre")
if buscar:
    datos = estudiantes.get(buscar)
    if
