import os
import json
import html

def cargar_json(ruta_json):
    """Carga y devuelve el contenido del archivo JSON."""
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_plantilla(ruta_plantilla):
    """Carga y devuelve la plantilla HTML."""
    with open(ruta_plantilla, 'r', encoding='utf-8') as f:
        return f.read()

def generar_html(contenido, plantilla):
    """Genera el HTML reemplazando los marcadores en la plantilla."""
    html = plantilla
    html = html.replace('<!--$TIPO$-->', contenido['tipo'])
    html = html.replace('<!--$TITULO$-->', contenido['titulo'])
    html = html.replace('<!--$AUTORA$-->', contenido['autor'])
    html = html.replace('<!--$FECHA$-->', contenido['fecha'])
    html = html.replace('<!--$DURACION$-->', contenido['duracion'])
    html = html.replace('<!--$DESCRIPCION$-->', contenido['descripcion'])
    html = html.replace('<!--$TEXTO$-->', contenido['texto'])
    return html

def guardar_html(nombre_archivo, html, carpeta_salida):
    """Guarda el HTML en la carpeta especificada con el nombre indicado."""
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta_salida = os.path.join(carpeta_salida, nombre_archivo)
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Archivo generado: {ruta_salida}")

def procesar_json_a_html(ruta_json, ruta_plantilla, carpeta_salida):
    """Procesa todas las entradas del JSON y genera sus archivos HTML."""
    data = cargar_json(ruta_json)
    plantilla = cargar_plantilla(ruta_plantilla)
    for key, contenido in data.items():
        html = generar_html(contenido, plantilla)
        guardar_html(f"{key}.html", html, carpeta_salida)

def procesar_descripcion(texto):
    """Convierte saltos de línea en párrafos HTML."""
    # Escapar HTML para seguridad
    texto = html.escape(texto.strip())

    # Reemplazar dos o más saltos de línea por cierre y apertura de párrafo
    texto = texto.replace("\n\n", "</p><p>")

    # Reemplazar saltos simples por espacio
    texto = texto.replace("\n", " ")

    # Envolver en etiquetas <p>
    return f'<p class="mb-3">{texto}</p>'

def procesar_texto(texto):
    """Convierte saltos de línea en párrafos HTML."""
    # Escapar HTML para seguridad
    texto = html.escape(texto.strip())

    # Reemplazar dos o más saltos de línea por cierre y apertura de párrafo
    texto = texto.replace("\n\n", "</p><p>")

    # Reemplazar saltos simples por espacio
    texto = texto.replace("\n", "</p><p>")

    # Envolver en etiquetas <p>
    return f"<p>{texto}</p>"

def leer_textos(carpeta):
    """Lee los archivos de texto de la carpeta y devuelve un diccionario con la información."""
    archivos_info = {}

    for nombre_archivo in sorted(os.listdir(carpeta)):
        if nombre_archivo.endswith(".txt"):
            ruta = os.path.join(carpeta, nombre_archivo)

            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read().strip()

            partes = contenido.split("$")

            if len(partes) >= 6:
                clave = os.path.splitext(nombre_archivo)[0]
                texto_completo = partes[5].strip()
                cantidad_palabras = len(texto_completo.split())
                archivos_info[clave] = {
                    "tipo": partes[0].strip(),
                    "titulo": partes[1].strip(),
                    "autor": partes[2].strip(),
                    "fecha": partes[3].strip(),
                    "duracion": (str(round(cantidad_palabras * 0.3 / 60, 2))+" min"),
                    "descripcion": procesar_descripcion(partes[4]),
                    # Aquí procesamos el texto a HTML con párrafos
                    "texto": procesar_texto(partes[5])
                }
            else:
                print(f"⚠ Archivo {nombre_archivo} no tiene el formato esperado.")

    return archivos_info

def guardar_json(archivos_info, salida):
    """Guarda la información en un archivo JSON."""
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(archivos_info, f, ensure_ascii=False, indent=4)
    print(f"\n✅ Información guardada en {salida}")


def main():
    carpeta_textos = "textos"  # Cambia por tu carpeta
    salida_json = "textos.json"

    archivos_info = leer_textos(carpeta_textos)
    guardar_json(archivos_info, salida_json)
    procesar_json_a_html('textos.json', 'plantilla_textos.html','../docs/material/textos')


if __name__ == "__main__":
    main()
