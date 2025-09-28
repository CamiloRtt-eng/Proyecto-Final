# Streamlit App: Gestión de Denuncias con Gemini

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from openpyxl import load_workbook

# --- 1. Preparación y Conexión de Datos ---

# Cargar clave Gemini
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

# Función para cargar XLSX y CSV con cache
@st.cache_data
def load_xlsx(path):
    return pd.read_excel(path)

@st.cache_data
def load_csv(path):
    return pd.read_csv(path, encoding="latin1", on_bad_lines='skip')

# Cargar datasets
legal_df = load_xlsx("DELITOS Y PENAS CLASIFICADAS.xlsx")
fiscalia_df = load_csv("BASE_DATOS_FISCALIA.csv")

# --- 2. Interfaz de Usuario y Formulario ---
# Mostrar columnas disponibles en la tabla legal para depuración
# Colores institucionales Fiscalía
st.markdown("""
    <style>
    .stButton button {
        background-color: #003366 !important;
        color: #fff !important;
        border-radius: 8px !important;
        border: 1px solid #003366 !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px #00336622;
        padding: 8px 24px;
        transition: background 0.2s;
    }
    .stButton button:hover {
        background-color: #0055a5 !important;
        border: 1px solid #0055a5 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Fondo blanco ya configurado en .streamlit/config.toml



header_logo, header_title = st.columns([1,5])
with header_logo:
    st.image("data/Logo_Fiscalia.png", width=100)
with header_title:
    st.markdown("<h1 style='color: #003366; display: flex; align-items: center; height: 100px; margin: 0;'>Receptor de Denuncias Fiscalía General de la Nación</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px; color:#333; margin-bottom:24px;'>Bienvenido al sistema de denuncias. Por favor, diligencie el formulario con información clara y precisa. Sus datos serán tratados con confidencialidad.</p>", unsafe_allow_html=True)
# Borde visible en los cuadros de texto
st.markdown("""
    <style>
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        border: 2px solid #003366 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Layout principal: botón de consulta a la izquierda y formulario en dos columnas con estilo


# Crear layout con columna exclusiva para consultas y el formulario aparte


# El formulario solo se crea una vez, fuera de cualquier columna anidada
with st.form("denuncia_form"):
    st.markdown("""
        <div style='background: #fff; border-radius: 16px; box-shadow: 0 2px 8px #00336622; padding: 24px 16px; margin-bottom: 16px;'>
            <h4 style='color:#0055a5; margin-top:0; margin-bottom:18px;'>No se quede callado, ¡Denuncie!</h4>
        """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        contenido = st.text_area("✍️ Contenido de la Denuncia", max_chars=2000, help="Describa los hechos de la denuncia")
        st.markdown("<style>.stTextArea textarea {border: 3px solid #0055a5 !important; background: #f5f7fa !important;}</style>", unsafe_allow_html=True)
        fecha = st.date_input("📅 Fecha de los Hechos", value=datetime.today())
        st.markdown("<style>.stDateInput input {border: 3px solid #0055a5 !important; background: #f5f7fa !important;}</style>", unsafe_allow_html=True)
        lugar = st.text_input("📍 Lugar de los Hechos")
    with col2:
        indiciado_nombre = st.text_input("👤 Nombre del Indiciado")
        indiciado_doc = st.text_input("🆔 Documento de Identidad del Indiciado")
        indiciado_email = st.text_input("✉️ Correo Electrónico del Indiciado")
    with col3:
        victima_nombre = st.text_input("👤 Nombre de la Víctima")
        victima_doc = st.text_input("🆔 Documento de Identidad de la Víctima")
        victima_email = st.text_input("✉️ Correo Electrónico de la Víctima")
    rol = st.radio("Rol del Usuario", ["Víctima", "Denunciante"], help="Seleccione su rol en la denuncia")
    submitted = st.form_submit_button("✅ Registrar Denuncia")
    st.markdown("</div>", unsafe_allow_html=True)

# Consulta de denuncias al final de la página


st.markdown("---")
st.markdown("<h3 style='color:#003366;'>Consultas</h3>", unsafe_allow_html=True)
# Botones en la misma fila
col_consultar, col_eliminar = st.columns([4,1])
with col_consultar:
    consultar = st.button("🔍 Consultar denuncias", help="Ver todas las denuncias registradas")
with col_eliminar:
    st.markdown("<style>.stButton button {padding: 4px 10px !important; font-size: 12px !important;}</style>", unsafe_allow_html=True)
    eliminar = st.button("🗑️", help="Eliminar todas las denuncias registradas")
file_path = os.path.join("data", "denuncias_registradas.xlsx")
if 'consultar' in locals() and consultar:
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        st.write("### Denuncias Registradas")
        st.dataframe(df)
    else:
        st.warning("No hay denuncias registradas aún.")
if 'eliminar' in locals() and eliminar:
    if os.path.exists(file_path):
        os.remove(file_path)
        st.success("Todas las denuncias han sido borradas.")
    else:
        st.info("No hay denuncias para borrar.")

# --- 3. Lógica de Análisis y Clasificación ---
def gemini_identifica_delitos(texto):
    # Aquí iría la llamada real a Gemini API
    # Simulación: retorna lista de delitos detectados
    return ["Robo", "Amenazas"]

def clasifica_delitos(delitos, legal_df):
    resultados = []
    # Diccionario de equivalencias
    equivalencias = {
        "robo": "Hurto"
    }
    for delito in delitos:
        delito_buscar = equivalencias.get(delito.lower(), delito)
        match = legal_df[legal_df["Articulo"].str.lower() == delito_buscar.lower()]
        if not match.empty:
            pena = match.iloc[0]["Pena Prision"] if "Pena Prision" in match.columns else "N/A"
            multa = match.iloc[0]["Multa"] if "Multa" in match.columns else "N/A"
            articulo = match.iloc[0]["Articulo"]
            resultados.append({
                "Delito": delito,
                "Pena Prision": pena,
                "Multa": multa,
                "Artículo": articulo
            })
        else:
            resultados.append({
                "Delito": delito,
                "Pena": "No encontrado",
                "Multa": "No encontrado",
                "Artículo": "No encontrado"
            })
    return resultados

if submitted and contenido:
    st.info("Analizando denuncia con Gemini...")
    delitos_detectados = gemini_identifica_delitos(contenido)
    st.success(f"Delitos identificados: {', '.join(delitos_detectados)}")
    clasificacion = clasifica_delitos(delitos_detectados, legal_df)
    st.write("### Clasificación Legal")
    st.dataframe(pd.DataFrame(clasificacion))

    # --- 4. Almacenamiento Persistente ---
    # Usar Articulo como Delito
    articulos = [c["Artículo"] if "Artículo" in c else c.get("Articulo","") for c in clasificacion]
    registro = {
        "Fecha": fecha,
        "Lugar": lugar,
        "Contenido": contenido,
        "Nombre del Indiciado": indiciado_nombre,
        "Documento de Identidad": indiciado_doc,
        "Correo del Indiciado": indiciado_email,
        "Rol": rol,
        "Nombre de la Víctima": victima_nombre,
        "Documento de Identidad de la Víctima": victima_doc,
        "Correo de la Víctima": victima_email,
        "Delitos": ", ".join(articulos),
        "Articulo": ", ".join(articulos),
        "Clasificacion": str(clasificacion)
    }
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, "denuncias_registradas.xlsx")
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = pd.concat([df, pd.DataFrame([registro])], ignore_index=True)
    else:
        df = pd.DataFrame([registro])
    # Reordenar y renombrar columnas para la consulta
    columnas_orden = [
        "Fecha", "Lugar", "Contenido", "Nombre del Indiciado", "Documento de Identidad", "Correo del Indiciado", "Rol",
        "Nombre de la Víctima", "Documento de Identidad de la Víctima", "Correo de la Víctima", "Delitos", "Articulo", "Clasificacion"
    ]
    df = df[columnas_orden]
    df.to_excel(file_path, index=False)
    st.success("Denuncia registrada y almacenada correctamente.")

# --- Consulta Total ---

# --- Consulta Total ---
# --- Consulta Total ---
# (Ahora la consulta se muestra en la columna izquierda)