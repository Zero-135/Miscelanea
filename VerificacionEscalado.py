import subprocess
import json
import cv2
import numpy as np
import os

def ffprobe(video):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,bit_rate:format=bit_rate",
        "-of", "json",
        video
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)

    stream = data["streams"][0]
    width = stream["width"]
    height = stream["height"]

    # Bitrate del stream
    stream_bitrate = stream.get("bit_rate", 0)
    stream_bitrate = int(stream_bitrate) if stream_bitrate not in (None, "", "0") else 0

    # Bitrate del formato (fallback)
    format_bitrate = data["format"].get("bit_rate", 0)
    format_bitrate = int(format_bitrate) if format_bitrate not in (None, "", "0") else 0

    bitrate = stream_bitrate if stream_bitrate > 0 else format_bitrate

    return width, height, bitrate


def freq_energy(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude = np.abs(fshift)

    h, w = magnitude.shape

    # Tomar un área del borde (alta frecuencia)
    border = magnitude[:h//10, :]  # 10% superior
    energy_high = np.mean(border)

    return energy_high


def analyze_fft(video, samples=8):
    cap = cv2.VideoCapture(video)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    values = []
    for i in np.linspace(0, total-1, samples, dtype=int):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            continue
        values.append(freq_energy(frame))

    cap.release()
    return np.mean(values) if values else 0


def detectar_upscale(video):
    width, height, bitrate = ffprobe(video)
    fft_value = analyze_fft(video)

    # Solo 1920×1080
    if (width, height) != (1920, 1080):
        return "No es 1920×1080"

    # Valores típicos FFT descubiertos en pruebas:
    # - 720p escalado → FFT alta frecuencia: 10–30
    # - 1080p comprimido → 30–70
    # - 1080p de alta calidad → 70–150+

    sospecha = []

    if bitrate < 3_000_000:
        sospecha.append("Bitrate bajo")

    if fft_value < 30:
        sospecha.append(f"Energía alta-frecuencia MUY baja ({fft_value:.1f}) → casi seguro escalado")
    elif fft_value < 50:
        sospecha.append(f"Energía alta-frecuencia baja ({fft_value:.1f}) → sospechoso")

    if sospecha:
        return "ESCALADO → " + ", ".join(sospecha)

    return f"OK (1080p real). FFT={fft_value:.1f}"


def analizar_carpeta_recursivo(ruta):
    extensiones = {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm"}

    for root, dirs, files in os.walk(ruta):
        for file in files:
            if os.path.splitext(file)[1].lower() in extensiones:
                full = os.path.join(root, file)
                print("\n▶", full)
                print(" ", detectar_upscale(full))


# --- EJECUTAR ---
carpeta = r"C:\Users\Walter Rivas\Documents\Videos\Demon Slayer S01 1080p Dual Audio BDRip 10 bits DD x265-EMBER"
analizar_carpeta_recursivo(carpeta)
