import os
import subprocess
import re


def renombrar():
    for root, dirs, files in os.walk(carpeta):
        for nombre in files:
            ruta_completa = os.path.join(root, nombre)

            # Calcular nuevo nombre
            nuevo_nombre = nombre.replace(buscar, reemplazar)

            # Si no cambia, saltar
            if nuevo_nombre == nombre:
                continue

            nueva_ruta = os.path.join(root, nuevo_nombre)

            print(f"Renombrando: {ruta_completa} -> {nueva_ruta}")
            os.rename(ruta_completa, nueva_ruta)


def limpiarMetadataMP4(carpeta):
    # Lista de metadatos comunes que queremos borrar (dejar vacíos)
    campos = [
        "title", "comment", "description", "genre", "artist",
        "album", "track", "date", "creation_time", "encoder",
        "album_artist", "composer", "lyrics",
        # versiones específicas de MP4 atoms
        "©nam", "©ART", "©alb", "©gen", "©day",
        # evitar que VLC lea marcas internas como título
        "major_brand", "minor_version", "compatible_brands"
    ]

    for root, dirs, files in os.walk(carpeta):
        for nombre in files:
            if nombre.lower().endswith(".mp4"):
                ruta = os.path.join(root, nombre)
                print("Limpiando metadata de:", ruta)

                temporal = ruta + ".tmp.mp4"

                # Construir parámetros de borrado
                borrar = []
                for campo in campos:
                    borrar.extend(["-metadata", f"{campo}="])

                # Ejecutar ffmpeg para limpiar metadata
                subprocess.run(
                    ["ffmpeg", "-i", ruta, "-map", "0", "-c", "copy"] +
                    borrar + [temporal],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )

                os.replace(temporal, ruta)
                print("✔ Metadata eliminada\n")


def obtener_pistas_mkv(ruta):
    try:
        r = subprocess.run(["mkvmerge", "-i", ruta], capture_output=True, text=True, check=True)
        salida = r.stdout.splitlines()
    except:
        return []

    ids = []
    for linea in salida:
        m = re.search(r"Track ID (\d+)", linea)
        if m:
            ids.append(int(m.group(1)))
    return ids


def limpiar_mkv():
    for root, dirs, files in os.walk(carpeta):
        for nombre in files:
            if not nombre.lower().endswith(".mkv"):
                continue

            ruta = os.path.join(root, nombre)
            print("\nProcesando:", ruta)

            pistas = obtener_pistas_mkv(ruta)
            print("  Pistas detectadas:", pistas)

            comandos = [
                "mkvpropedit", ruta,
                "--delete", "title",      # borra titulo del MKV
                "--tags", "all:"          # borra TODOS los TAGS
            ]

            for i in pistas:
                comandos += [
                    "--edit", f"track:@{i}",
                    "--delete", "name",
                    "--tags", f"track:@{i}:"  # borra TAGS de la pista
                ]

            try:
                subprocess.run(comandos, check=True)
                print("  → Título y TAGS eliminados correctamente")
            except Exception as e:
                print("  ERROR:", e)


carpeta = r"C:\Users\Walter Rivas\Documents\Videos\Konosuba\Nueva carpeta"
buscar = "Demon Slayer - "
reemplazar = ""
# [NewbSubs]
# Moozzi2

# renombrar()
limpiarMetadataMP4(carpeta)
limpiar_mkv()