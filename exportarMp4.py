import os
import subprocess

carpeta = r"C:\Users\Walter Rivas\Downloads\Nueva carpeta (3)"

for archivo in os.listdir(carpeta):
    if archivo.lower().endswith(".mkv"):
        ruta_mkv = os.path.join(carpeta, archivo)
        ruta_mp4 = ruta_mkv.replace(".mkv", ".mp4")

        print(f"Convirtiendo: {archivo}")

        # Convertir a formato C:/... (requerido por FFmpeg dentro del filtro)
        ruta_ffmpeg = ruta_mkv.replace("\\", "/")

        # Filtro correcto para subtítulos internos (SRT o ASS)
        filtro = f"subtitles='{ruta_ffmpeg}'"

        comando = [
            "ffmpeg",
            "-y",
            "-i", ruta_mkv,
            "-vf", filtro,
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "medium",
            "-c:a", "aac",
            "-b:a", "192k",
            ruta_mp4
        ]

        subprocess.run(comando, shell=True)

print("Completado.")
