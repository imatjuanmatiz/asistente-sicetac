import spacy

nlp = spacy.load("es_core_news_sm")

def extraer_parametros(texto):
    doc = nlp(texto.lower())

    lugares = [ent.text.title() for ent in doc.ents if ent.label_ == "LOC"]
    if len(lugares) < 2:
        import re
        lugares = re.findall(r"de ([A-ZÁÉÍÓÚa-záéíóú]+) a ([A-ZÁÉÍÓÚa-záéíóú]+)", texto, re.IGNORECASE)
        if lugares:
            lugares = list(lugares[0])
    if len(lugares) < 2:
        raise ValueError("No se pudieron identificar el origen y destino")

    import re, datetime
    configuracion = None
    match_config = re.search(r"\b(C[23]S?[23]?)\b", texto.upper())
    if match_config:
        configuracion = match_config.group(1)

    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5,
        "junio": 6, "julio": 7, "agosto": 8, "septiembre": 9,
        "octubre": 10, "noviembre": 11, "diciembre": 12
    }

    mes = None
    for palabra in texto.lower().split():
        if palabra in meses:
            mes = meses[palabra]
            break

    if mes:
        ahora = datetime.datetime.now()
        año = ahora.year
        mes_compuesto = año * 100 + mes
    else:
        mes_compuesto = datetime.datetime.now().year * 100 + datetime.datetime.now().month

    return {
        "origen": lugares[0],
        "destino": lugares[1],
        "configuracion": configuracion,
        "mes": mes_compuesto
    }
