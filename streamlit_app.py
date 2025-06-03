import streamlit as st
import json
import os

# Archivo de base de datos
DB_FILE = "estudiantes.json"

# Usuarios autorizados
USUARIOS = {
    "Nicolas Medina": {"rol": "propietario", "clave": "admin2013"},
    "Tomas Maldonado": {"rol": "administrador", "clave": "admin143"},
    "Simon Romoleroux": {"rol": "administrador", "clave": "admin133"},
    "Eva Godoy": {"rol": "administradora", "clave": "admin3"},
}

# Consejos según estilo
consejos = {
    "visual": "Usa mapas mentales, diagramas y colores para enseñar.",
    "auditivo": "Habla en voz alta, usa canciones o rimas.",
    "kinestésico": "Incorpora movimiento, juegos físicos o manualidades.",
    "lector/escritor": "Usa listas, resúmenes y escritura repetida."
}

# Cargar datos
def cargar_estudiantes():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

# Guardar datos
def guardar_estudiantes(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Login
def login():
    st.sidebar.title("🔐 Iniciar sesión")
    usuario = st.sidebar.text_input("Usuario")
    clave = st.sidebar.text_input("Contraseña", type="password")
    if usuario in USUARIOS and clave == USUARIOS[usuario]["clave"]:
        return usuario, USUARIOS[usuario]["rol"]
    elif usuario and clave:
        st.sidebar.error("Usuario o contraseña incorrectos")
    return None, None

# Interfaz principal
st.title("🎓 Base de Datos: Estilos de Aprendizaje")

# Cargar base de datos
estudiantes = cargar_estudiantes()

usuario, rol = login()

if usuario:
    st.success(f"Bienvenido, {usuario} ({rol})")

    # Añadir o editar estudiante
    st.subheader("➕ Añadir o Editar estudiante")
    nombre = st.text_input("Nombre del estudiante")
    genero = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])
    estilo = st.selectbox("Estilo de aprendizaje", list(consejos.keys()))
    if st.button("Guardar estudiante"):
        if nombre:
            estudiantes[nombre] = {"genero": genero, "estilo": estilo}
            guardar_estudiantes(estudiantes)
            st.success(f"{nombre} guardado correctamente")
        else:
            st.warning("El nombre es obligatorio")

    st.divider()

    # Buscar estudiante
    st.subheader("🔍 Buscar estudiante")
    buscar = st.text_input("Buscar por nombre")
    if buscar:
        datos = estudiantes.get(buscar)
        if datos:
            st.info(f"{buscar} — género: {datos['genero']} — estilo: {datos['estilo']}")
            st.write("💡 Consejo:", consejos[datos['estilo']])
            if rol == "propietario":
                if st.button("Eliminar estudiante"):
                    estudiantes.pop(buscar)
                    guardar_estudiantes(estudiantes)
                    st.warning(f"{buscar} fue eliminado.")
        else:
            st.error("Estudiante no encontrado")

    st.divider()

    # Lista de todos
    st.subheader("📋 Lista de todos los estudiantes")
    if estudiantes:
        for nombre, datos in estudiantes.items():
            st.write(f"**{nombre}** — género: {datos['genero']} — estilo: *{datos['estilo']}*")
    else:
        st.info("No hay estudiantes registrados.")
else:
    st.info("Por favor, inicia sesión para acceder a la base de datos.")
