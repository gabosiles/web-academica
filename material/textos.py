import os
import json
import html
import random

def cargar_json(ruta_json):
    """Carga y devuelve el contenido del archivo JSON."""
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_plantilla(ruta_plantilla):
    """Carga y devuelve la plantilla HTML."""
    with open(ruta_plantilla, 'r', encoding='utf-8') as f:
        return f.read()

def generar_html(contenido, plantilla, id_articulo, N):
    """Genera el HTML reemplazando los marcadores en la plantilla."""
    html = plantilla
    html = html.replace('<!--$TIPO$-->', contenido['tipo'])
    html = html.replace('<!--$TITULO$-->', contenido['titulo'])
    html = html.replace('<!--$AUTORA$-->', contenido['autor'])
    html = html.replace('<!--$FECHA$-->', contenido['fecha'])
    html = html.replace('<!--$DURACION$-->', contenido['duracion'])
    html = html.replace('<!--$DESCRIPCION$-->', contenido['descripcion'])
    html = html.replace('<!--$TEXTO$-->', contenido['texto'])
    # Reemplazar la imagen usando el ID del artículo
    num = random.randint(0, N)
    img_PERFIL_html = f'<img class="rounded-circle" src="../../assets/img/perfiles/{num}.jpg" width="70">'
    html = html.replace('<!--$IMGPERFIL$-->', img_PERFIL_html)
    img_TEXT_html = f'<img src="../../assets/img/textos/{id_articulo}.jpg">'
    html = html.replace('<!--$IMGTEXT$-->', img_TEXT_html)


    return html

def guardar_html(nombre_archivo, html, carpeta_salida):
    """Guarda el HTML en la carpeta especificada con el nombre indicado."""
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta_salida = os.path.join(carpeta_salida, nombre_archivo)
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Archivo generado: {ruta_salida}")

def procesar_json_a_html(ruta_json, ruta_plantilla, carpeta_salida, N):
    """Procesa todas las entradas del JSON y genera sus archivos HTML."""
    data = cargar_json(ruta_json)
    plantilla = cargar_plantilla(ruta_plantilla)
    for key, contenido in data.items():
        html = generar_html(contenido, plantilla, key, N)
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

def generar_bloque_secciones(contenido, id_articulo):
    """Genera un bloque HTML por cada artículo del JSON."""
    bloque = f"""<!--Bloque de Articulo {id_articulo}-->
<div class="mb-3 d-flex justify-content-between">
    <div class="pr-3">
        <h2 class="mb-1 h4 font-weight-bold">
            <a class="text-danger">{contenido['tipo']}</a>
        </h2>
        <h2 class="mb-1 h4 font-weight-bold">
            <a class="text-dark" href="./material/textos/{id_articulo}.html">{contenido['titulo']}</a>
        </h2>
        {contenido['descripcion']}
        <div class="font-weight-bold">{contenido['autor']}</div>
        <small class="text-muted">{contenido['fecha']} · {contenido['duracion']}</small>
    </div>
    <img height="140" src="./assets/img/textos/{id_articulo}.jpg" class="imagen-cuadro">
</div>
<h1 class="font-weight-bold spanborder"></h1>
"""
    return bloque

def generar_secciones_html(ruta_json, ruta_plantilla, ruta_salida):
    """Genera el archivo final HTML reemplazando $SECCIONES$ en la plantilla."""
    data = cargar_json(ruta_json)
    plantilla = cargar_plantilla(ruta_plantilla)

    # Generar todos los bloques
    bloques = "\n".join(generar_bloque_secciones(contenido, id_articulo) 
                        for id_articulo, contenido in data.items())

    # Reemplazar marcador en plantilla
    html_final = plantilla.replace("<!--$SECCIONES$-->", bloques)

    # Guardar archivo final
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html_final)

    print(f"Archivo generado en: {ruta_salida}")

def main():
    carpeta_textos = "textos"  # Cambia por tu carpeta
    salida_json = "textos.json"

    archivos_info = leer_textos(carpeta_textos)
    guardar_json(archivos_info, salida_json)
    procesar_json_a_html('textos.json', 'plantilla_textos.html','../docs/material/textos', 10)
    generar_secciones_html('./textos.json', './plantilla_secciones.html', '../docs/secciones.html')

if __name__ == "__main__":
    main()
