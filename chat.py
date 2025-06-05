import pandas as pd
from asistente_sicetac import responder_consulta_sicetac

print("🔄 Cargando datos...")
rutas_df = pd.read_excel("RUTA_DISTANCIA_LIMPIO.xlsx")
municipios_df = pd.read_excel("municipios.xlsx")
matriz_parametros = pd.read_excel("MATRIZ_CAMBIOS_PARAMETROS_LIMPIO.xlsx")
matriz_costos_fijos = pd.read_excel("COSTO_FIJO_ACTUALIZADO.xlsx")
matriz_vehicular = pd.read_excel("CONFIGURACION_VEHICULAR_LIMPIO.xlsx")
peajes_df = pd.read_excel("PEAJES_LIMPIO.xlsx")

print("✅ Asistente SICETAC listo. Escribe 'salir' para terminar.\\n")

while True:
    mensaje = input("🧑‍💼 Tú: ")
    if mensaje.lower() in ["salir", "exit", "quit"]:
        print("👋 Hasta luego.")
        break

    respuesta = responder_consulta_sicetac(
        mensaje,
        rutas_df,
        municipios_df,
        matriz_parametros,
        matriz_costos_fijos,
        matriz_vehicular,
        peajes_df
    )
    print(respuesta)
