import yt_dlp
import os


def descargar_h264_con_aac(url):
    os.makedirs(folder_name, exist_ok=True)

    opciones = {
        # Forzar video AVC/H.264 y audio AAC
        "format": "bv*[vcodec*=avc1]+ba[acodec~=mp4a]/b[ext=mp4]",

        "outtmpl": folder_name + "/%(title)s.%(ext)s",

        "postprocessors": [
            {
                "key": "FFmpegVideoRemuxer",
                "preferedformat": "mp4"
            }
        ]
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])

    print("Descargado: Video H.264 + AAC (100% compatible).")


# Ejemplo

folder_name = "Videos"
txt_name = "ListaUrlYoutube.txt"

with open(txt_name, "r", encoding="utf-8") as f:
    for linea in f:
        descargar_h264_con_aac(linea)