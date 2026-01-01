import os

carpeta = r"C:\Users\Walter Rivas\Documents\Videos\[BDrip] Sword Art Online Alternative GGO S02 [7³ACG]\Nueva carpeta"
#Boku No Hero S01E
#Boku No Hero SP01E
#Boku No Hero OVA
#Boku No Hero MOV
#Boku No Hero SM

archivos = sorted(os.listdir(carpeta))
contador = 1
nombreFinal = "[Zero Anime] Alternative Gun Gale S02E"

for archivo in archivos:
    ruta_completa = os.path.join(carpeta, archivo)

    if os.path.isfile(ruta_completa):
        _, extension = os.path.splitext(archivo)
        nombre = nombreFinal

        numero = f"{contador:02d}"  # 01, 02, 03...
        nuevo_nombre = f"{nombre}{numero}{extension}"
        nueva_ruta = os.path.join(carpeta, nuevo_nombre)

        os.rename(ruta_completa, nueva_ruta)
        contador += 1

print("Renombrado completado.")
