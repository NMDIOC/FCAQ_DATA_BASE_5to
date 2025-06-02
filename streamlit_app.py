import streamlit as st
import json
import os

DB_FILE = "estudiantes.json"

# Base de consejos por estilo
consejos = {
    "visual": "Usa mapas mentales, diagramas y colores para enseñar.",
    "auditivo": "Habla en voz alta, usa canciones o rimas.",
    "kinestésico": "Incorpora movimiento, juegos físicos o manualidades.",
    "lector/escritor": "Usa listas, resúmenes y escritura repetida."
}

# Usuarios permitidos
usuarios_autorizados = {
    "Nicolas Medina": {"rol": "propietario", "clave": "Admin2013"},
    "Tomas Maldonado": {"rol": "admin", "clave": "FCAQ_DATABASE"},
    "Simon Romoleroux": {"rol": "admin", "clave": "FCAQ_DATABASE"},
    "Eva Godoy": {"rol": "admin", "clave": "FCAQ_DATABASE"},
}

# Cargar y guardar datos
def cargar_estudiantes():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_estudiantes(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Login con usuario y contraseña
def login():
    st.sidebar.title("🔐 Iniciar sesión")
    usuario = st.sidebar.selectbox("Selecciona tu usuario", list(usuarios_autorizados.keys()))
    clave = st.sidebar.text_input("Contraseña", type="password")

    if clave:
        if clave == usuarios_autorizados[usuario]["clave"]:
            return usuario, usuarios_autorizados[usuario]["rol"]
        else:
            st.sidebar.error("Contraseña incorrecta")
    return None, None

# Interfaz principal
st.title("🎓 Base de Datos: Estilos de Aprendizaje")

usuario, rol = login()
estudiantes = cargar_estudiantes()

if usuario:
    st.success(f"Bienvenido {usuario} ({rol})")

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

st.subheader("🔍 Buscar estudiante")
buscar = st.text_input("Buscar por nombre")
if buscar:
    datos = estudiantes.get(buscar)
    if datos:
        estilo = datos["estilo"]
        st.info(f"{buscar} tiene un estilo de aprendizaje **{estilo}**")
        st.write("💡 Consejo:", consejos[estilo])

        if rol == "propietario" and st.button("Eliminar estudiante"):
            estudiantes.pop(buscar)
            guardar_estudiantes(estudiantes)
            st.warning(f"{buscar} fue eliminado de la base de datos")
    else:
        st.error("Estudiante no encontrado")

st.subheader("📋 Lista de todos los estudiantes")
if estudiantes:
    for nombre, datos in estudiantes.items():
        st.write(f"**{nombre}** — estilo: *{datos['estilo']}*")
else:
    st.info("Todavía no hay estudiantes registrados.")
