import streamlit as st
import json
import os

# Archivo para guardar los datos
DB_FILE = "estudiantes.json"

# Usuarios y contraseñas autorizadas
USUARIOS = {
    "Nicolas Medina": {"rol": "propietario", "clave": "Sabu3319"},
    "Tomas Maldonado": {"rol": "administrador", "clave": "admin123"},
    "Simon Romoleroux": {"rol": "administrador", "clave": "admin123"},
    "Eva Godoy": {"rol": "administrador", "clave": "admin123"},
}

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

# Validar los datos
def validar_datos_estudiantes(data):
    estilos_validos = {"visual", "auditivo", "kinestésico", "lector/escritor"}
    generos_validos = {"Masculino", "Femenino"}

    errores = []
    for nombre, datos in data.items():
        if not isinstance(datos, dict):
            errores.append(f"{nombre}: No es un diccionario.")
            continue
        if "estilo" not in datos:
            errores.append(f"{nombre}: Falta la clave 'estilo'.")
        elif datos["estilo"] not in estilos_validos:
            errores.append(f"{nombre}: Estilo inválido '{datos['estilo']}'.")
        if "genero" not in datos:
            errores.append(f"{nombre}: Falta la clave 'genero'.")
        elif datos["genero"] not in generos_validos:
            errores.append(f"{nombre}: Género inválido '{datos['genero']}'.")
    return errores

# Login
def login():
    st.sidebar.title("🔐 Iniciar sesión")
    usuario = st.sidebar.text_input("Usuario")
    clave = st.sidebar.text_input("Contraseña", type="password")
    if usuario in USUARIOS and clave == USUARIOS[usuario]["clave"]:
        return usuario, USUARIOS[usuario]["rol"]
    elif clave:
        st.sidebar.error("Usuario o contraseña incorrectos")
    return None, None

# Interfaz principal
st.title("🎓 Base de Datos: Estilos de Aprendizaje")
estudiantes = cargar_estudiantes()

# Validación de datos
errores = validar_datos_estudiantes(estudiantes)
if errores:
    st.warning("⚠️ Errores en la base de datos:")
    for err in errores:
        st.text("• " + err)
    st.stop()

usuario, rol = login()

if usuario:
    st.success(f"Bienvenido {usuario} ({rol}) 👋")

    # Solo admins pueden añadir o editar
    if rol in ["administrador", "propietario"]:
        st.subheader("➕ Añadir o editar estudiante")
        nombre = st.text_input("Nombre del estudiante")
        estilo = st.selectbox("Estilo de aprendizaje", list(consejos.keys()))
        genero = st.selectbox("Género", ["Masculino", "Femenino"])
        if st.button("Guardar estudiante"):
            if nombre:
                estudiantes[nombre] = {"estilo": estilo, "genero": genero}
                guardar_estudiantes(estudiantes)
                st.success(f"{nombre} ha sido guardado o actualizado")
            else:
                st.warning("Por favor, escribí un nombre")

    st.divider()

    # Buscar estudiante
    st.subheader("🔍 Buscar estudiante")
    buscar = st.text_input("Buscar por nombre")
    if buscar:
        resultado = estudiantes.get(buscar)
        if resultado:
            st.info(f"{buscar} tiene un estilo de aprendizaje **{resultado['estilo']}**")
            st.write("💡 Consejo:", consejos[resultado['estilo']])
            if rol == "propietario":
                if st.button("Eliminar estudiante"):
                    estudiantes.pop(buscar)
                    guardar_estudiantes(estudiantes)
                    st.warning(f"{buscar} fue eliminado")
        else:
            st.error("Estudiante no encontrado")

    st.divider()

# Mostrar todos (público o logueado)
st.subheader("📋 Lista de todos los estudiantes")
if estudiantes:
    for nombre, datos in estudiantes.items():
        st.write(f"**{nombre}** — estilo: *{datos['estilo']}*, género: {datos['genero']}")
else:
    st.info("Todavía no hay estudiantes registrados")
