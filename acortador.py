from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def obtener_link_final(url_inicial):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url_inicial)
    print("[*] Cargando página...")

    # Esperar redirección interna (auditmy.link usa un temporizador)
    time.sleep(5)

    # Buscar automáticamente el botón que lleva al siguiente link
    try:
        boton = WebDriverWait(driver, 12).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='btn-go' or contains(@href,'go')]"))
        )
        boton.click()
        print("[*] Botón encontrado y clickeado.")
    except:
        print("[!] No encontré el botón, intentando permitir redirección automática...")

    # Esperar redirección
    time.sleep(5)

    # Manejar pestaña nueva
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

    final = driver.current_url
    driver.quit()
    return final


# EJEMPLO DE USO CON TU LINK
print(obtener_link_final("http://app.auditmy.link//i/c7bhn"))
