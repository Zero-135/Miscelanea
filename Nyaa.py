import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from openpyxl import Workbook
import os


def mainPage(urlPage):
    page = urllink(urlPage)

    #if page.status_code == 502 or page.status_code == 520 \
    #        or page.status_code == 504:
    if page.status_code != 200:
        return mainPage(urlPage)

    soup = BeautifulSoup(page.content, 'html.parser')

    div = soup.find("div", "table-responsive")
    if div is None:
        return []

    table = div.find("table")
    tbody = table.find("tbody")
    trList = tbody.find_all("tr")

    anime = []

    for tr in trList:
        tds = tr.find_all("td")

        tdName = tds[1]
        href = urlBase + tdName.find("a")["href"]
        name = tdName.get_text().strip()

        magnet = tds[2]
        lenSpan = len(magnet.find_all("a"))
        magnetHref = magnet.find_all("a")[lenSpan - 1]["href"]

        size = tds[3].get_text().strip()
        if "K" in size:
            size = size.replace("KiB", "")
            size = float(size)/(1000*1000)
        elif "M" in size:
            size = size.replace("MiB", "")
            size = float(size)/1000
        elif "T" in size:
            size = size.replace("TiB", "")
            size = float(size)*1000
        else:
            size = size.replace("GiB", "")
            size = float(size)

        seeders = int(tds[5].get_text().strip())
        fecha = datetime.fromisoformat(tds[4].get_text().strip())
        fecha_menos_X = fecha - timedelta(hours=5)

        obj = {
            "linkAnime": urlPage,
            "name": name,
            "link": href,
            "size": size,
            "fecha": fecha_menos_X.strftime("%Y-%m-%d %H:%M:%S"),
            "seeders": seeders,
            "magnet": magnetHref
        }

        anime.append(obj)

    return anime



def urllink(url):
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
        "User-Agent": "Mozilla/5.0"
    }
    try:
        return requests.get(url, headers=headers)
    except:
        print("Error")
        return urllink(url)


urlBase = "https://nya.iss.one"
urlExample = "https://nya.iss.one/?f=0&c=0_0&q=%22Dr.+Stone%22+BD&s=id&o=desc"
input_txt = "links.txt"
output_dir = "Excel"
os.makedirs(output_dir, exist_ok=True)

with open(input_txt, "r", encoding="utf-8") as file:
    for linea in file:

        urlTxt = (
            "https://nya.iss.one/?f=0&c=0_0&q=%22"
            + linea.strip().replace(" ", "+").replace(",","%2C")
            + "%22+BD&s=id&o=desc"
        )

        datos = mainPage(urlTxt)

        wb = Workbook()
        ws = wb.active
        ws.title = "Datos"

        # Encabezados
        ws.append(["linkAnime", "Nombre", "Link", "Size", "Fecha", "Seeders", "Magnet"])

        # Filtros
        ws.auto_filter.ref = "A1:G1"

        for item in datos:
            ws.append([
                item["linkAnime"],
                item["name"],
                item["link"],
                item["size"],
                item["fecha"],
                item["seeders"],
                item["magnet"]
            ])

        # Autoajuste columnas
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter

            if col_letter in ("A", "C", "F", "G"):
                continue

            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))

            ws.column_dimensions[col_letter].width = max_length + 2

        nombre_excel = os.path.join(
            output_dir,
            linea.strip().replace("/", "_") + ".xlsx"
        )

        wb.save(nombre_excel)
