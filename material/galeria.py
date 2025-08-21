import os
import json
import html

def leer_texto(ruta_txt):
    """Lee un archivo de texto y devuelve sus partes separadas por $"""
    with open(ruta_txt, "r", encoding="utf-8", errors="replace") as f:
        contenido = f.read().strip()
    partes = [p.strip() for p in contenido.split("$")]

    if len(partes) >= 6:
        return {
            "titulo": partes[1],
            "autor": partes[2],
            "fecha": partes[3],
            "descripcion": partes[5]
        }
    else:
        print(f"⚠ Archivo {ruta_txt} no tiene el formato esperado. Partes: {len(partes)}")
        return None


def procesar_carpeta(carpeta_textos, salida_json):
    """Recorre texts/ y genera JSON con rutas de imágenes en docs/assets/img/galeria/"""
    data = {}

    for archivo in sorted(os.listdir(carpeta_textos)):
        if archivo.endswith(".txt"):
            clave = os.path.splitext(archivo)[0]
            ruta_txt = os.path.join(carpeta_textos, archivo)

            info = leer_texto(ruta_txt)
            if info:
                # 🔹 Ruta relativa correcta desde docs/
                info["imagen"] = f"./assets/img/galeria/{clave}.jpg"
                data[clave] = info

    with open(salida_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ JSON generado en {salida_json}")


# ==========================
# 🔹 Generar HTML desde JSON
# ==========================
def generar_html(json_file, plantilla_file, salida_html):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(plantilla_file, "r", encoding="utf-8") as f:
        plantilla = f.read()

    imagenes_html = ""
    for idx, (clave, item) in enumerate(data.items()):
        # 🔹 Escapar caracteres especiales para que no rompan el HTML
        titulo = html.escape(item["titulo"])
        autor = html.escape(item["autor"])
        fecha = html.escape(item["fecha"])
        descripcion = html.escape(item["descripcion"])

        imagenes_html += f'''
        <img src="{item["imagen"]}" data-texto="
            <div class='titulo'>{titulo}</div>
            <div class='autor'>{autor}</div>
            <div class='fecha'>{fecha}</div>
            <div class='descripcion'>{descripcion}</div>
        " onclick="abrirLightbox({idx})">
        '''

    html_final = plantilla.replace("<!--IMAGENES-->", imagenes_html)

    with open(salida_html, "w", encoding="utf-8") as f:
        f.write(html_final)

    print(f"✅ HTML generado en {salida_html}")


if __name__ == "__main__":
    # Ahora los textos los lees desde material/galeria/texts
    carpeta_textos = "./galeria/texts"

    # JSON e HTML se generan en docs/
    salida_json = "../docs/assets/json/ilustraciones.json"
    plantilla_file = "plantilla_galeria.html"
    salida_html = "../docs/ilustraciones.html"

    procesar_carpeta(carpeta_textos, salida_json)
    generar_html(salida_json, plantilla_file, salida_html)
