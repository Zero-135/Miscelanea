import subprocess
import os


def reducir_peso_mkv(input_file, output_file, crf, preset):
    comando = [
        "ffmpeg",
        "-i", input_file,
        "-c:v", "libx264",
        "-crf", str(crf),
        "-preset", preset,
        "-c:a", "copy",
        "-c:s", "copy",
        "-y",
        output_file
    ]
    subprocess.run(comando, check=True)


def quemar_subtitulo(input_file, output_file, subtitle_index):
    # Escapar la ruta para Windows
    input_escaped = input_file.replace("\\", "/").replace(":", "\\:")

    comando = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"subtitles='{input_escaped}':si={subtitle_index}",
        "-c:a", "copy",
        "-y",  # sobrescribe si ya existe
        output_file
    ]

    result = subprocess.run(comando, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Error en {os.path.basename(input_file)}:")
        print(result.stderr)
    else:
        print(f"✅ {os.path.basename(input_file)} convertido correctamente")


def procesar_carpeta(entrada_folder, salida_folder):
    if not os.path.exists(salida_folder):
        os.makedirs(salida_folder)

    for archivo in os.listdir(entrada_folder):
        if archivo.lower().endswith(".mkv"):
            input_path = os.path.join(entrada_folder, archivo)
            #output_path = os.path.join(salida_folder, archivo)

            output_file = os.path.splitext(archivo)[0] + ".mp4"
            output_path = os.path.join(salida_folder, output_file)

            print(f"Procesando {archivo}...")
            #reducir_peso_mkv(input_path, output_path, 23, "slow")
            quemar_subtitulo(input_path, output_path, 0)
            print(f"✅ {archivo} completado")


# ==================== USO ====================
entrada = r"D:\Anime\Uma Musume Pretty Derby[BD]\4.2.-Uma Musume Pretty Derby - Shin Jidai no Tobira"
salida = r"C:\Users\win11\Videos\Anime"

procesar_carpeta(entrada, salida)