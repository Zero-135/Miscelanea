import os
from PIL import Image
from openpyxl import Workbook


def main():
    # Crear un nuevo libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Dimensiones de Imágenes"

    # Encabezados
    ws.append(["Nombre de archivo", "Ancho (px)", "Alto (px)"])

    # Recorrer archivos de la carpeta
    for nombre_archivo in os.listdir(carpeta_imagenes):
        ruta_completa = os.path.join(carpeta_imagenes, nombre_archivo)

        # Intentar abrir como imagen
        try:
            ancho = 0
            alto = 0
            with Image.open(ruta_completa) as img:
                ancho, alto = img.size
                ws.append([nombre_archivo, ancho, alto])
        except IOError:
            print(f"Archivo ignorado (no es imagen): {nombre_archivo}")

    # Guardar el archivo Excel
    ruta_salida = os.path.join(carpeta_imagenes, "dimensiones_imagenes.xlsx")
    wb.save(ruta_salida)
    print(f"Archivo Excel creado en: {ruta_salida}")


def excelNombre():
    # Crear un nuevo libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Dimensiones de Imágenes"

    # Encabezados
    ws.append(["Nombre de archivo"])


    # Leer las reglas de renombrado del txt
    reemplazos = {}
    with open(nuevo_txt, 'r', encoding='utf-8') as f:
        for linea in f:
            if '#' in linea:
                nuevo, viejo = linea.strip().split('#', 1)
                reemplazos[viejo.strip()] = nuevo.strip()

    # Renombrar los archivos
    for archivo in os.listdir(carpeta_imagenes):
        ruta_archivo = os.path.join(carpeta_imagenes, archivo)
        if os.path.isfile(ruta_archivo):
            nombre_sin_ext, ext = os.path.splitext(archivo)
            barra = ""
            partes = nombre_sin_ext.split("_")
            tam = len(partes)
            nombre_sin_barra = ""

            if tam == 1:
                nombre_sin_barra = partes[0]
            else:
                if tam == 2:
                    nombre_sin_barra = partes[0]
                    barra = "_" + partes[1]
                else:
                    print(nombre_sin_ext)

            # Buscar qué parte del nombre coincide con las claves del diccionario
            for viejo, nuevo in reemplazos.items():
                new_name = viejo.upper().replace(" ", "").replace("'", "").replace("-", "").replace(".", "")
                if new_name == nombre_sin_barra:
                    nuevo_nombre = nombre_sin_barra.replace(new_name, nuevo) + barra + ext
                    # nuevo_nombre = nombre_sin_barra.replace(new_name, nuevo) + ext
                    ruta_nueva = os.path.join(carpeta_imagenes, nuevo_nombre)
                    # print(f'Renombrado: {archivo} → {nuevo_nombre}')
                    ws.append([nombre_sin_barra + "-" + nuevo_nombre])
                    break  # Solo se renombra con la primera coincidencia

    # Guardar el archivo Excel
    ruta_salida = os.path.join(carpeta_imagenes, "dimensiones_imagenes.xlsx")
    wb.save(ruta_salida)
    print(f"Archivo Excel creado en: {ruta_salida}")



# Ruta de la carpeta que contiene las imágenes
carpeta_imagenes = r'C:\Users\Walter Rivas\Downloads\Pokes\Pokemon\Front'  # <- Reemplaza con tu ruta
nuevo_txt = r'D:\PycharmProjects\MyAnimeList\Projects\NamePokemon.txt'

excelNombre()