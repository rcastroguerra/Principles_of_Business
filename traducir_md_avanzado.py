from deep_translator import GoogleTranslator
import os

translator = GoogleTranslator(source='auto', target='es')

def traducir_texto(texto):
    try:
        return translator.translate(texto)
    except:
        return texto

def es_codigo(linea):
    return linea.strip().startswith("```")

def es_url(linea):
    return "http://" in linea or "https://" in linea

def es_html(linea):
    return linea.strip().startswith("<") and linea.strip().endswith(">")

def traducir_linea(linea):
    # No traducir código, URLs ni HTML
    if es_url(linea) or es_html(linea):
        return linea

    # Tablas: traducir solo el texto entre |
    if "|" in linea and not linea.strip().startswith("```"):
        partes = linea.split("|")
        nuevas = []
        for p in partes:
            contenido = p.strip()
            if contenido and "---" not in contenido:
                nuevas.append(" " + traducir_texto(contenido) + " ")
            else:
                nuevas.append(p)
        return "|".join(nuevas)

    # Listas y títulos: traducir después del símbolo
    if linea.strip().startswith(("#", "-", "*", "+", ">")):
        simbolo = linea[:linea.index(linea.lstrip())]
        contenido = linea.lstrip()
        return simbolo + traducir_texto(contenido)

    # Párrafos normales
    return traducir_texto(linea)

def traducir_markdown(entrada, salida):
    with open(entrada, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    traducidas = []
    dentro_codigo = False

    for linea in lineas:
        if es_codigo(linea):
            dentro_codigo = not dentro_codigo
            traducidas.append(linea)
            continue

        if dentro_codigo:
            traducidas.append(linea)
        else:
            traducidas.append(traducir_linea(linea))

    with open(salida, "w", encoding="utf-8") as f:
        f.writelines(traducidas)

    print(f"Archivo traducido guardado como: {salida}")


# Ejecutar
traducir_markdown("entrada.md", "salida_traducida.md")