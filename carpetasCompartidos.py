import os
import pandas as pd

DISCO = r"H:\\"
SALIDA = "carpetas_disco_G.xlsx"

filas = []

# 🔹 Solo primer nivel (NO recursivo)
for item in os.listdir(DISCO):
    ruta_completa = os.path.join(DISCO, item)

    if os.path.isdir(ruta_completa):
        filas.append([
            item.replace("[BD]", ""),
            ruta_completa
        ])

df = pd.DataFrame(filas, columns=[
    "Nombre de carpeta",
    "Ruta completa"
])

ruta_excel = os.path.abspath(SALIDA)
df.to_excel(ruta_excel, index=False)

# 🔹 Abrir Excel al final
os.startfile(ruta_excel)

print("Proceso finalizado correctamente.")
