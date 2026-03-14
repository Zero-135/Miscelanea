import os
import re


def buscar_funcion_en_clases(rutas_carpetas, nombre_clase, nombre_funcion, extensiones=None):
    if extensiones is None:
        extensiones = []

    if isinstance(rutas_carpetas, str):
        rutas_carpetas = [rutas_carpetas]

    archivos_encontrados = []

    for ruta_base in rutas_carpetas:

        for root, dirs, files in os.walk(ruta_base):
            for file in files:

                if extensiones and not any(file.endswith(ext) for ext in extensiones):
                    continue

                ruta_completa = os.path.join(root, file)

                try:
                    with open(ruta_completa, "r", encoding="utf-8", errors="ignore") as f:
                        lineas = f.readlines()

                    dentro_clase = False
                    nivel = 0
                    encontrada_en_archivo = False

                    for linea in lineas:
                        linea_strip = linea.strip()

                        # Detectar EXACTAMENTE: class Battle
                        if not dentro_clase and re.match(
                                rf"^(class|module)\s+{re.escape(nombre_clase)}\s*$",
                                linea_strip
                        ):
                            dentro_clase = True
                            nivel = 1
                            continue

                        if dentro_clase:

                            # Detectar método buscado
                            if re.match(
                                    rf"^def\s+{re.escape(nombre_funcion)}\b",
                                    linea_strip
                            ):
                                encontrada_en_archivo = True

                            # Si abre nuevo bloque
                            if re.match(r"^(class|module|def)\b", linea_strip):
                                nivel += 1

                            # Si cierra bloque
                            if linea_strip == "end":
                                nivel -= 1
                                if nivel == 0:
                                    dentro_clase = False

                    if encontrada_en_archivo:
                        archivos_encontrados.append(ruta_completa)

                except Exception as e:
                    print(f"Error leyendo {ruta_completa}: {e}")

    if archivos_encontrados:
        print("\nArchivos encontrados:\n")
        for archivo in archivos_encontrados:
            print(archivo)
    else:
        print("\nNo se encontraron coincidencias.")


# =========================
# EJEMPLO DE USO
# =========================

if __name__ == "__main__":
    rutas = [
        r"C:\Users\Walter Rivas\Documents\PokeProject V4\Data\Scripts",
        r"C:\Users\Walter Rivas\Documents\PokeProject V4\Plugins"
    ]

    clase = "Battle"
    funcion = "pbAbilityTriggered"

    buscar_funcion_en_clases(rutas, clase, funcion, extensiones=[".rb"])