import streamlit as st
import json
import os

DB_FILE = "estudiantes.json"

# Función para cargar base de datos
def cargar_datos():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

# Función para guardar base de datos
def guardar_datos(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Usuarios registrados
usuarios = {
    "Nicolas Medina": {"rol": "propietario", "contraseña": "Sabu3319"},
    "Tomas Maldonado": {"rol": "administrador", "contraseña": "admin133"},
    "Simon Romoleroux": {"rol": "administrador", "contraseña": "admin122"},
    "Eva Godoy": {"rol": "administradora", "contraseña": "Turo8404!"},
    "invitado": {"rol": "invitado", "contraseña": "invitado123"}
}

st.set_page_config(page_title="Base de Datos de Estilos", layout="centered")
st.title("🎓 Base de Datos: Estilos de Aprendizaje")

# Login
st.sidebar.header("🔐 Iniciar sesión")
usuario = st.sidebar.selectbox("Selecciona tu usuario", list(usuarios.keys()))
clave_ingresada = st.sidebar.text_input("Contraseña", type="password")

# Verificación de usuario
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
            st.write(f"**{nombre}** — paralelo: {datos['paralelo']} — estilo: *{datos['estilo']}*")
    elif busqueda:
        st.info("No se encontraron resultados")

    # Mostrar todos
    st.subheader("📋 Lista de todos los estudiantes")
    if db:
        for nombre, datos in db.items():
            st.write(f"**{nombre}** — paralelo: {datos['paralelo']} — estilo: *{datos['estilo']}*")
    else:
        st.info("No hay estudiantes registrados")

    # Modo admin
    if rol != "invitado":
        st.sidebar.header("⚙️ Administrar estudiantes")
        modo = st.sidebar.selectbox("Acción", ["Agregar o editar", "Eliminar"])

        nombre = st.sidebar.text_input("Nombre del estudiante")
        paralelo = st.sidebar.selectbox("Paralelo", ["A", "B", "C", "D", "E", "F"])
        estilo = st.sidebar.selectbox("Estilo de aprendizaje", ["Visual", "Auditivo", "Kinestésico", "Lector/Escritor"])

        if modo == "Agregar o editar":
            if st.sidebar.button("Guardar"):
                if nombre:
                    db[nombre] = {"paralelo": paralelo, "estilo": estilo}
                    guardar_datos(db)
                    st.sidebar.success("Estudiante guardado correctamente")
                else:
                    st.sidebar.warning("El nombre no puede estar vacío")

        elif modo == "Eliminar":
            if rol == "propietario":
                if nombre in db:
                    if st.sidebar.button("Eliminar"):
                        del db[nombre]
                        guardar_datos(db)
                        st.sidebar.success("Estudiante eliminado")
                elif nombre:
                    st.sidebar.warning("Nombre no encontrado")
            else:
                st.sidebar.warning("Solo el propietario puede eliminar estudiantes")

else:
    st.warning("🔒 Ingresa una contraseña válida para acceder")
