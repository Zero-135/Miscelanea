from PIL import Image
import os

carpeta_entrada = r"C:\Users\Walter Rivas\Documents\Imagenes\Pokemon\Back shiny"
carpeta_salida = r"C:\Users\Walter Rivas\Documents\PokeProject\Graphics\Pokemon\Back shiny"

os.makedirs(carpeta_salida, exist_ok=True)

extensiones = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

for archivo in os.listdir(carpeta_entrada):
    if archivo.lower().endswith(extensiones):
        ruta = os.path.join(carpeta_entrada, archivo)

        with Image.open(ruta) as img:
            ancho, alto = img.size
            nuevo_ancho = int(ancho * 2 / 3)
            nuevo_alto = int(alto * 2 / 3)

            img_redimensionada = img.resize(
                (nuevo_ancho, nuevo_alto),
                Image.LANCZOS
            )

            salida = os.path.join(carpeta_salida, archivo)
            img_redimensionada.save(salida)

print("✅ Imágenes redimensionadas a 2/3")