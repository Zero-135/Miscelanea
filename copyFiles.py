import os
import shutil
from pathlib import Path
import cv2
import pandas as pd
import time
import datetime


def getmusic():
    direc = list(sorted(Path("C:\\Users\\Walter Rivas\\Music\\Audio-Anime").iterdir(), key=os.path.getctime, reverse=True))

    dir = "C:\\Users\\Walter Rivas\\Music\\Audio-Anime\\Copy\\"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    for folder in direc:
        if folder.name == "Copy":
            continue
        filesMp3 = [f.name for f in os.scandir(folder) if f.is_file()]
        for file in filesMp3:
            nameSplit = file.split(".-")
            name = ""

            if len(nameSplit) > 1:
                name = nameSplit[1]
            else:
                name = nameSplit[0]

            source = "C:\\Users\\Walter Rivas\\Music\\Audio-Anime\\" + folder.name + "\\" + file
            target = "C:\\Users\\Walter Rivas\\Music\\Audio-Anime\\Copy\\" + folder.name + " - " + file
            # target = "C:\\Users\\Walter Rivas\\Music\\Audio-Anime\\Copy\\" + name
            shutil.copyfile(source, target)


def getresolution(folder_path):
    try:
        for ele in os.scandir(folder_path):
            name = ele.name
            path = ele.path

            if name.find(".jpg") != -1 or name.find(".png") != -1:
                continue

            if os.path.isdir(path):
                getresolution(path)
            else:
                vid = cv2.VideoCapture(path)
                size = os.path.getsize(path)
                height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
                width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
                frame = vid.get(cv2.CAP_PROP_FPS)

                year = int(time.strftime("%Y",time.strptime(time.ctime(os.path.getmtime(ele)))))
                month = int(time.strftime("%m",time.strptime(time.ctime(os.path.getmtime(ele)))))
                day = int(time.strftime("%d",time.strptime(time.ctime(os.path.getmtime(ele)))))
                dateCreation = datetime.date(year=year, day=day, month=month)

                nameList.append(name)
                heightList.append(height)
                widthList.append(width)
                frameList.append(frame)
                creationList.append(dateCreation)
                sizeList.append(size)
    except NameError:
        print(NameError)


def getExcel():
    df = pd.DataFrame({"Nombre": nameList, "Altura": heightList, "Ancho": widthList, "Frames": frameList,
                       "Fecha": creationList, "Peso": sizeList})
    df.to_excel("Excel\\Resolution.xlsx", index=False)
    os.system("Excel\\Resolution.xlsx")


nameList = list()
heightList = list()
widthList = list()
frameList = list()
creationList = list()
sizeList = list()
getmusic()
#getresolution(r"C:\Users\Walter Rivas\Documents\Openings 2")
#getExcel()
