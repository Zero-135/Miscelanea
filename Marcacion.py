from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from selenium.webdriver.common.alert import Alert


def clickear(button):
    # ================================
    # CONFIGURACIÓN
    # ================================

    URL = "https://app.canvia.com/marcacion/m_portal_empleado/sm_marcacion/rea_marcacion.aspx"  # ← cambia esto
    USUARIO = "wrivas@canvia.com"
    PASSWORD = "Lima2025$"

    ID_USUARIO = "txtUsuario"  # ← cambia según tu página
    ID_PASSWORD = "txtContrasenia"  # ← cambia según tu página
    ID_BOTON_LOGIN = "btnIngresar"  # ← cambia según tu página
    ID_BOTON_CLICKEAR = button  # ← botón a presionar luego

    # ================================
    # PROGRAMA
    # ================================

    # Iniciar navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(URL)
    time.sleep(1)

    # 1. Ingresar usuario
    driver.find_element(By.ID, ID_USUARIO).send_keys(USUARIO)

    # 2. Ingresar contraseña
    driver.find_element(By.ID, ID_PASSWORD).send_keys(PASSWORD)

    # 3. Presionar botón login
    driver.find_element(By.ID, ID_BOTON_LOGIN).click()

    time.sleep(2)  # esperar carga de la página

    # 4. Presionar el botón REANUDAR
    try:
        driver.find_element(By.ID, ID_BOTON_CLICKEAR).click()
    except:
        # A veces el botón está oculto en ASP.NET → hacemos click por JS
        driver.execute_script(
            f"document.getElementById('{ID_BOTON_CLICKEAR}').click()"
        )

    if button == buttonSalida:
        alert = Alert(driver)
        alert.accept()  # Presiona "Aceptar"

    print("✔ Botón presionado correctamente")
    time.sleep(3)

    driver.quit()


def clickearV2(button):
    # ================================
    # CONFIGURACIÓN
    # ================================

    URL = "https://app.canvia.com/marcacion/m_portal_empleado/sm_marcacion/rea_marcacion.aspx"  # ← cambia esto
    USUARIO = "wrivas@canvia.com"
    PASSWORD = "Lima2025$"

    ID_USUARIO = "txtUsuario"  # ← cambia según tu página
    ID_PASSWORD = "txtContrasenia"  # ← cambia según tu página
    ID_BOTON_LOGIN = "btnIngresar"  # ← cambia según tu página
    ID_BOTON_CLICKEAR = button  # ← botón a presionar luego

    # ================================
    # NAVEGADOR HEADLESS (SIN VENTANA)
    # ================================
    opts = Options()
    opts.add_argument("--headless=new")  # Chrome Headless moderno
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )

    driver.get(URL)
    time.sleep(1)

    # 1. Usuario
    driver.find_element(By.ID, ID_USUARIO).send_keys(USUARIO)

    # 2. Contraseña
    driver.find_element(By.ID, ID_PASSWORD).send_keys(PASSWORD)

    # 3. Login
    try:
        driver.find_element(By.ID, ID_BOTON_LOGIN).click()
    except:
        driver.execute_script(
            f"document.getElementById('{ID_BOTON_LOGIN}').click()"
        )
    time.sleep(2)

    # 4. Presionar botón
    try:
        driver.find_element(By.ID, ID_BOTON_CLICKEAR).click()
    except:
        driver.execute_script(
            f"document.getElementById('{ID_BOTON_CLICKEAR}').click()"
        )

    if button == buttonSalida:
        alert = Alert(driver)
        alert.accept()  # Presiona "Aceptar"

    print("✔ Botón presionado sin abrir ninguna ventana")
    time.sleep(3)

    driver.quit()


def definirBoton():
    # hora = datetime.now().strftime("%H:%M:%S")
    # solo_hora = datetime.now().strftime("%H")
    hora = datetime.now().hour

    match hora:
        case h if 0 <= h < 12:
            clickearV2(buttonEntrada)
        case h if 12 <= h < 14:
            clickearV2(inicioRefrigerio)
        case h if 14 <= h < 16:
            clickearV2(finRefrigerio)
        case h if 16 <= h < 23:
            clickearV2(buttonSalida)


buttonEntrada = 'ctl00_body_inpbutEntrada'
inicioRefrigerio = 'ctl00_body_inpbutPausar'
finRefrigerio = 'ctl00_body_inpbutReanudar'
buttonSalida = 'ctl00_body_inpbutSalida'

definirBoton()