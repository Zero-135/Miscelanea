import os
import subprocess
import pandas as pd
from pathlib import Path


def getFilse(path):
    try:
        for ele in os.scandir(path):
            name = ele.name
            path = ele.path
            if os.path.isdir(path):
                if not (name in listNoProcces):
                    getFilse(path)
            else:
                execute(name, path)
    except:
        print(path)


def execute(name, path):
    process = subprocess.Popen([exe, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)
    listName.append(path)
    i = 0
    try:
        for output in process.stdout:
            if output.strip() == "Subtitle:" or i > 0:
                if i == 1:
                    listSub.append(output.strip())
                i = i + 1
    except:
        print(path)
    if i == 0:
        listSub.append("")


def excel(name):
    df = pd.DataFrame({"Nombre": listName, "Subs": listSub})
    df.to_excel(name, index=False)
    os.system(name)


def getList(name):
    my_file = open(baseTxt + name, "r")
    data = my_file.read()
    my_file.close()
    return data.split("\n")


baseTxt = "Txts\\"
input_file = ["G:/", "H:/"]
input_file2 = "Tokyo Ghoul-Forzado.mkv"
listNoProcces = getList("listNoProcces.txt")
exe = "hachoir-metadata"
exe2 = "exiftool.exe"
listName = list()
listSub = list()
for i in input_file:
    direc = sorted(Path(i).iterdir(), key=os.path.getctime, reverse=True)
    filtered = filter(lambda fichero: "[BD]" in os.path.basename(fichero), direc)
    listBD = list(filtered)
    for l in listBD:
        getFilse(l)
excel("Excel\\Subs.xlsx")
