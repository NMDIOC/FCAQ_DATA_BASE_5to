import streamlit as st
import json
import os

DB_FILE = "estudiantes.json"

consejos = {
    "visual": "Usa mapas mentales, diagramas y colores para enseñar.",
    "auditivo": "Habla en voz alta, usa canciones o rimas.",
    "kinestésico": "Incorpora movimiento, juegos físicos o manualidades.",
    "lector/escritor": "Usa listas, resúmenes y escritura repetida."
}

def cargar_estudiantes():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_estudiantes(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def login():
    st.sidebar.title("🔐 Iniciar sesión")
    clave = st.sidebar.text_input("Contraseña de administrador", type="password")
    if clave == "FCAQ_DATABASE":
        return True
    elif clave != "":
        st.sidebar.error("Contraseña incorrecta")
    return False

st.title("🎓 Base de Datos: Estilos de Aprendizaje")

estudiantes = cargar_estudiantes()
es_admin = login()

if es_admin:
    st.success("Bienvenido administrador 👋")

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

    st.divider()

st.subheader("🔍 Buscar estudiante")
buscar = st.text_input("Buscar por nombre")
if buscar:
    datos = estudiantes.get(buscar)
    if datos:
        estilo = datos["estilo"]
        genero = datos["genero"]
        emoji = "🧒" if genero == "Masculino" else "👧"
        st.info(f"{emoji} {buscar} tiene un estilo de aprendizaje **{estilo}**")
        st.write("💡 Consejo:", consejos[estilo])

        if es_admin and st.button("Eliminar estudiante"):
            estudiantes.pop(buscar)
            guardar_estudiantes(estudiantes)
            st.warning(f"{buscar} fue eliminado de la base de datos")
    else:
        st.error("Estudiante no encontrado")

st.divider()

st.subheader("📋 Lista de todos los estudiantes")
if estudiantes:
    for nombre, datos in estudiantes.items():
        emoji = "🧒" if datos["genero"] == "Masculino" else "👧"
        st.write(f"{emoji} **{nombre}** — estilo: *{datos['estilo']}*")
else:
    st.info("Todavía no hay estudiantes registrados.")
