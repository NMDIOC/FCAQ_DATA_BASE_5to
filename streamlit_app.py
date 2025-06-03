import streamlit as st
import json
import os

DB_FILE = "estudiantes.json"

# Función para cargar base de datos
def cargar_datos():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Función para guardar base de datos
def guardar_datos(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Lista de usuarios y contraseñas
usuarios = {
    "Nicolas Medina": {"rol": "propietario", "contraseña": "admin2013"},
    "Tomas Maldonado": {"rol": "administrador", "contraseña": "admin133"},
    "Simon Romoleroux": {"rol": "administrador", "contraseña": "admin122"},
    "Eva Godoy": {"rol": "administradora", "contraseña": "admin3"},
    "invitado": {"rol": "invitado", "contraseña": "invitado123"}
}

st.set_page_config(page_title="Base de Datos de Estilos", layout="centered")
st.title("🎓 Base de Datos: Estilos de Aprendizaje")

# Autenticación
st.sidebar.header("🔐 Iniciar sesión")
usuario = st.sidebar.selectbox("Selecciona tu usuario", list(usuarios.keys()))
clave_ingresada = st.sidebar.text_input("Contraseña", type="password")

if clave_ingresada == usuarios[usuario]["contraseña"]:
    rol = usuarios[usuario]["rol"]
    st.sidebar.success(f"Sesión iniciada como {usuario} ({rol})")
    db = cargar_datos()

    # Buscar estudiante
    st.subheader("🔍 Buscar estudiante")
    busqueda = st.text_input("Buscar por nombre")

    resultados = {nombre: datos for nombre, datos in db.items() if busqueda.lower() in nombre.lower()}

    if resultados:
        for nombre, datos in resultados.items():
            st.write(f"**{nombre}** — género: {datos['genero']} — estilo: *{datos['estilo']}*")

    # Mostrar todos
    st.subheader("📋 Lista de todos los estudiantes")
    for nombre, datos in db.items():
        st.write(f"**{nombre}** — género: {datos['genero']} — estilo: *{datos['estilo']}*")

    # Modo administrador (menos para invitados)
    if rol != "invitado":
        st.sidebar.markdown("---")
        st.sidebar.header("⚙️ Administrar estudiantes")

        modo = st.sidebar.selectbox("Acción", ["Agregar o editar", "Eliminar"])

        nombre = st.sidebar.text_input("Nombre del estudiante")
        genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino", "Otro"])
        estilo = st.sidebar.text_input("Estilo de aprendizaje")

        if modo == "Agregar o editar":
            if st.sidebar.button("Guardar"):
                db[nombre] = {"genero": genero, "estilo": estilo}
                guardar_datos(db)
                st.sidebar.success("Estudiante guardado correctamente")

        elif modo == "Eliminar":
            if rol == "propietario":
                if nombre in db:
                    if st.sidebar.button("Eliminar"):
                        del db[nombre]
                        guardar_datos(db)
                        st.sidebar.success("Estudiante eliminado")
                else:
                    st.sidebar.warning("Nombre no encontrado en la base de datos")
            else:
                st.sidebar.warning("Solo el propietario puede eliminar estudiantes")

else:
    st.warning("🔒 Ingresa la contraseña correcta para acceder")
