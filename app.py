import streamlit as st
import pandas as pd
from asistente_sicetac import responder_consulta_sicetac

# Configuración de la página
st.set_page_config(page_title="Asistente SICETAC", page_icon="🚛")
st.title("🛣️ Asistente de Costos de Transporte SICETAC")

# Cargar datos con manejo de errores
@st.cache_data
def cargar_datos():
    try:
        rutas = pd.read_excel("RUTA_DISTANCIA_LIMPIO.xlsx")
        municipios = pd.read_excel("municipios.xlsx")
        parametros = pd.read_excel("MATRIZ_CAMBIOS_PARAMETROS_LIMPIO.xlsx")
        costos_fijos = pd.read_excel("COSTO_FIJO_ACTUALIZADO.xlsx")
        vehiculos = pd.read_excel("CONFIGURACION_VEHICULAR_LIMPIO.xlsx")
        peajes = pd.read_excel("PEAJES_LIMPIO.xlsx")
        return rutas, municipios, parametros, costos_fijos, vehiculos, peajes
    except Exception as e:
        st.error(f"Error al cargar archivos: {e}")
        st.stop()  # Detiene la app si hay errores

# Interfaz
mensaje = st.text_input(
    "Escribe tu consulta:",
    placeholder="Ej: ¿Cuánto cuesta ir de Bogotá a Medellín con un C3S3 en junio 2025?"
)

if st.button("Calcular") and mensaje:
    with st.spinner("Procesando..."):
        try:
            datos = cargar_datos()
            respuesta = responder_consulta_sicetac(mensaje, *datos)
            st.success("✅ Resultado:")
            st.markdown(respuesta)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
