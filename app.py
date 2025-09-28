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
    return pd.read_csv(path, encoding="latin1")

# Cargar datasets
legal_df = load_xlsx("DELITOS Y PENAS CLASIFICADAS.xlsx")
fiscalia_df = load_csv("BASE_DATOS_FISCALIA.csv")

# --- 2. Interfaz de Usuario y Formulario ---
st.title("Gestión de Denuncias - Fiscalía + IA Gemini")
st.write("Registra, analiza y consulta denuncias de forma inteligente.")

with st.form("denuncia_form"):
    st.subheader("Registro de Denuncia")
    contenido = st.text_area("Contenido de la Denuncia", max_chars=2000)
    fecha = st.date_input("Fecha de los Hechos", value=datetime.today())
    lugar = st.text_input("Lugar de los Hechos")
    indiciado_nombre = st.text_input("Nombre del Indiciado")
    indiciado_doc = st.text_input("Documento de Identidad del Indiciado")
    indiciado_email = st.text_input("Correo Electrónico del Indiciado")
    rol = st.radio("Rol del Usuario", ["Víctima", "Denunciante"])
    if rol == "Denunciante":
        victima_nombre = st.text_input("Nombre de la Víctima")
        victima_doc = st.text_input("Documento de Identidad de la Víctima")
        victima_email = st.text_input("Correo Electrónico de la Víctima")
    else:
        victima_nombre = victima_doc = victima_email = ""
    submitted = st.form_submit_button("Registrar Denuncia")

# --- 3. Lógica de Análisis y Clasificación ---
def gemini_identifica_delitos(texto):
    # Aquí iría la llamada real a Gemini API
    # Simulación: retorna lista de delitos detectados
    return ["Robo", "Amenazas"]

def clasifica_delitos(delitos, legal_df):
    resultados = []
    for delito in delitos:
        match = legal_df[legal_df["Delito"].str.lower() == delito.lower()]
        if not match.empty:
            pena = match.iloc[0]["Pena"]
            multa = match.iloc[0].get("Multa", "N/A")
            articulo = match.iloc[0]["Artículo"]
            resultados.append({
                "Delito": delito,
                "Pena": pena,
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
    registro = {
        "Fecha": fecha,
        "Lugar": lugar,
        "Contenido": contenido,
        "Indiciado_Nombre": indiciado_nombre,
        "Indiciado_Doc": indiciado_doc,
        "Indiciado_Email": indiciado_email,
        "Rol": rol,
        "Victima_Nombre": victima_nombre,
        "Victima_Doc": victima_doc,
        "Victima_Email": victima_email,
        "Delitos": ", ".join(delitos_detectados),
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
    df.to_excel(file_path, index=False)
    st.success("Denuncia registrada y almacenada correctamente.")

# --- Consulta Total ---
st.write("---")
if st.button("Consultar todas las denuncias"):
    file_path = os.path.join("data", "denuncias_registradas.xlsx")
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        st.write("### Denuncias Registradas")
        st.dataframe(df)
    else:
        st.warning("No hay denuncias registradas aún.")