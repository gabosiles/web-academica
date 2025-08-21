import os
from PIL import Image, ImageOps

# Evitar error por imágenes enormes
Image.MAX_IMAGE_PIXELS = None  

def optimizar_imagenes(carpeta_imagenes, max_size=(1600, 1600), calidad=80):
    for archivo in os.listdir(carpeta_imagenes):
        if archivo.lower().endswith((".jpg", ".jpeg", ".png")):
            ruta = os.path.join(carpeta_imagenes, archivo)
            try:
                with Image.open(ruta) as img:
                    # 🔹 Corrige orientación según metadatos EXIF
                    img = ImageOps.exif_transpose(img)

                    # 🔹 Redimensiona
                    img.thumbnail(max_size)

                    # 🔹 Manejo de transparencia en PNG → RGB fondo blanco
                    if img.mode == "RGBA":
                        fondo = Image.new("RGB", img.size, (255, 255, 255))
                        fondo.paste(img, mask=img.split()[3])
                        img = fondo
                    else:
                        img = img.convert("RGB")

                    # 🔹 Sobrescribe optimizada
                    img.save(ruta, "JPEG", quality=calidad, optimize=True)

                print(f"✅ Optimizada: {archivo}")
            except Exception as e:
                print(f"❌ Error con {archivo}: {e}")


if __name__ == "__main__":
    carpeta = "./galeria/images"  # cambia según tu ruta
    optimizar_imagenes(carpeta)
