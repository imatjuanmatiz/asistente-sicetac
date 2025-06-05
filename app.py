import streamlit as st
import pandas as pd
from asistente_sicetac import responder_consulta_sicetac

# Cargar los datos una sola vez
@st.cache_data
def cargar_datos():
    rutas = pd.read_excel("RUTA_DISTANCIA_LIMPIO.xlsx")
    municipios = pd.read_excel("municipios.xlsx")
    parametros = pd.read_excel("MATRIZ_CAMBIOS_PARAMETROS_LIMPIO.xlsx")
    costos_fijos = pd.read_excel("COSTO_FIJO_ACTUALIZADO.xlsx")
    vehiculos = pd.read_excel("CONFIGURACION_VEHICULAR_LIMPIO.xlsx")
    peajes = pd.read_excel("PEAJES_LIMPIO.xlsx")
    return rutas, municipios, parametros, costos_fijos, vehiculos, peajes

# Cargar insumos
rutas_df, municipios_df, matriz_parametros, matriz_costos_fijos, matriz_vehicular, peajes_df = cargar_datos()

# Interfaz de usuario
st.title("🛣️ Asistente SICETAC")
st.markdown("Consulta rutas y costos logísticos en lenguaje natural")

mensaje = st.text_input("Escribe tu pregunta:", placeholder="Ejemplo: ¿Cuánto cuesta ir de Bogotá a Medellín con un C3 en junio?")

if mensaje:
    with st.spinner("Calculando..."):
        respuesta = responder_consulta_sicetac(
            mensaje,
            rutas_df,
            municipios_df,
            matriz_parametros,
            matriz_costos_fijos,
            matriz_vehicular,
            peajes_df
        )
    st.markdown("### Respuesta")
    st.write(respuesta)
