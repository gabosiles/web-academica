import os
import chardet

def convertir_a_utf8(carpeta, carpeta_salida=None):
    """
    Convierte todos los archivos .txt de una carpeta a UTF-8.
    
    Args:
        carpeta: Carpeta de entrada
        carpeta_salida: Carpeta de salida (si es None, sobreescribe los archivos originales)
    """
    if carpeta_salida is None:
        carpeta_salida = carpeta
    else:
        os.makedirs(carpeta_salida, exist_ok=True)

    for nombre_archivo in os.listdir(carpeta):
        if nombre_archivo.endswith(".txt"):
            ruta = os.path.join(carpeta, nombre_archivo)

            # Leer archivo en binario y detectar encoding
            with open(ruta, "rb") as f:
                raw = f.read()
                resultado = chardet.detect(raw)
                encoding_detectado = resultado["encoding"]

            if encoding_detectado is None:
                print(f"⚠ No se pudo detectar encoding de {nombre_archivo}, se asume UTF-8")
                encoding_detectado = "utf-8"

            try:
                texto = raw.decode(encoding_detectado)
            except Exception as e:
                print(f"❌ Error al decodificar {nombre_archivo} con {encoding_detectado}: {e}")
                continue

            # Guardar en UTF-8
            ruta_salida = os.path.join(carpeta_salida, nombre_archivo)
            with open(ruta_salida, "w", encoding="utf-8") as f:
                f.write(texto)

            print(f"✅ {nombre_archivo} convertido de {encoding_detectado} a UTF-8")

if __name__ == "__main__":
    # Carpeta de entrada (donde están tus .txt)
    carpeta_entrada = "textos"
    
    # Opción 1: sobrescribir los archivos originales
    convertir_a_utf8(carpeta_entrada)

    # Opción 2: guardar en carpeta aparte
    # convertir_a_utf8(carpeta_entrada, "textos_utf8")
