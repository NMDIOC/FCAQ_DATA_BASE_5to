import streamlit as st
import json
import os

# Archivo para guardar los datos
DB_FILE = "estudiantes.json"

# Consejos por estilo
consejos = {
    "visual": "Usa mapas mentales, diagramas y colores para enseñar.",
    "auditivo": "Habla en voz alta, usa canciones o rimas.",
    "kinestésico": "Incorpora movimiento, juegos físicos o manualidades.",
    "lector/escritor": "Usa listas, resúmenes y escritura repetida."
}

# Cargar base de datos
def cargar_estudiantes():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

# Guardar base de datos
def guardar_estudiantes(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Login de admin
def login():
    st.sidebar.title("🔐 Iniciar sesión")
    clave = st.sidebar.text_input("Contraseña de administrador", type="password")
    if clave == "FCAQ_DATABASE":
        return True
    elif clave != "":
        st.sidebar.error("Contraseña incorrecta")
    return False

# Título principal
st.title("🎓 Base de Datos: Estilos de Aprendizaje")

# Cargar datos
estudiantes = cargar_estudiantes()

if login():
    st.success("Bienvenido administrador 👋")

    # Añadir estudiante
    st.subheader("➕ Añadir estudiante")
    nombre = st.text_input("Nombre del estudiante")
    estilo = st.selectbox("Estilo de aprendizaje", list(consejos.keys()))
    if st.button("Guardar estudiante"):
        if nombre:
            estudiantes[nombre] = estilo
            guardar_estudiantes(estudiantes)
            st.success(f"{nombre} ha sido guardado con estilo '{estilo}'")
        else:
            st.warning("Por favor, escribí un nombre")

    st.divider()

    # Buscar estudiante por nombre
    st.subheader("🔍 Buscar estudiante")
    buscar = st.text_input("Buscar por nombre")
    if buscar:
        resultado = estudiantes.get(buscar)
        if resultado:
            st.info(f"{buscar} tiene un estilo de aprendizaje **{resultado}**")
            st.write("💡 Consejo:", consejos[resultado])
            if st.button("Eliminar estudiante"):
                estudiantes.pop(buscar)
                guardar_estudiantes(estudiantes)
                st.warning(f"{buscar} fue eliminado de la base de datos")
        else:
            st.error("Estudiante no encontrado")

    st.divider()

    # Mostrar todos los estudiantes
    st.subheader("📋 Lista de todos los estudiantes")
    if estudiantes:
        for nombre, estilo in estudiantes.items():
            st.write(f"🧒 **{nombre}** — estilo: *{estilo}*")
    else:
        st.info("Todavía no hay estudiantes registrados")
