from parser_sicetac import extraer_parametros
from modelo_sicetac import calcular_modelo_sicetac_extendido

def responder_consulta_sicetac(
    mensaje,
    rutas_df,
    municipios_df,
    matriz_parametros,
    matriz_costos_fijos,
    matriz_vehicular,
    peajes_df
):
    try:
        from sicetac_helper import SICETACHelper
        params = extraer_parametros(mensaje)

        helper = SICETACHelper(municipios_df, matriz_vehicular)
        existe, cod_origen, cod_destino, fila_ruta_df = helper.ruta_existe(
            params["origen"], params["destino"], rutas_df
        )

        if not existe:
            return f"❌ No encontré una ruta registrada entre {params['origen']} y {params['destino']}."

        fila_ruta = fila_ruta_df.iloc[0]
        distancias = {
            "KM_PLANO": fila_ruta["KM_PLANO"],
            "KM_ONDULADO": fila_ruta["KM_ONDULADO"],
            "KM_MONTAÑOSO": fila_ruta["KM_MONTAÑOSO"],
            "KM_URBANO": fila_ruta["KM_URBANO"],
            "KM_DESPAVIMENTADO": fila_ruta["KM_DESPAVIMENTADO"]
        }

        resultado = calcular_modelo_sicetac_extendido(
            origen=params["origen"],
            destino=params["destino"],
            configuracion=params["configuracion"],
            serie=params["mes"],
            distancias=distancias,
            valor_peaje_manual=None,
            matriz_parametros=matriz_parametros,
            matriz_costos_fijos=matriz_costos_fijos,
            matriz_vehicular=matriz_vehicular,
            rutas_df=rutas_df,
            peajes_df=peajes_df,
            carroceria_especial="GENERAL",
            ruta_oficial=fila_ruta
        )

        return f"""
✅ Resultado para {resultado['configuracion']} de {resultado['origen']} a {resultado['destino']} ({resultado['mes']}):

- Horas de recorrido: {resultado['horas_recorrido']}h + {resultado['horas_logisticas']}h logísticas
- Recorridos al mes: {resultado['recorridos_mes']}
- Costo fijo por viaje: ${resultado['costo_fijo']:,.0f}
- Combustible: ${resultado['combustible']:,.0f}
- Peajes: ${resultado['peajes']:,.0f}
- Mantenimiento: ${resultado['mantenimiento']:,.0f}
- Imprevistos: ${resultado['imprevistos']:,.0f}
- Otros costos: ${resultado['otros_costos']:,.0f}

💰 **Total estimado del viaje**: ${resultado['total_viaje']:,.0f}
"""
    except Exception as e:
        return f"❌ No pude calcular el viaje. Error: {e}"
