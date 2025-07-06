from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time
import sys
import glob
import os

sys.path.append("..")

from config.driver_config import get_driver
from utils.pdf_report import generar_pdf_completo

# Limpia la carpeta de screenshots antes de correr el test
for file in glob.glob("../evidencia/screenshots/*.png"):
    os.remove(file)

# Variables de prueba
step_name = "Flujo Login en sistema local"
status = "PASSED"
color_status = (0, 128, 0)
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
steps = []
screenshot_path = f"../evidencia/screenshots/step_inicio_{int(time.time())}.png"
pdf_path = f"../evidencia/pdfs/evidencia_login_{status}_{int(time.time())}.pdf"

# Sigue tu código normal
driver = get_driver()
driver.get("http://localhost/control/login.php")

# ...

driver.get("http://localhost/control/login.php")

try:
    # Paso 1
    detalle = "Usuario ingresado correctamente."
    screenshot_path = f"../evidencia/screenshots/step_usuario_{int(time.time())}.png"
    driver.find_element(By.NAME, "user_name").send_keys("admin")
    driver.save_screenshot(screenshot_path)
    steps.append((detalle, screenshot_path))

    # Paso 2
    detalle = "Contraseña ingresada correctamente."
    screenshot_path = f"../evidencia/screenshots/step_password_{int(time.time())}.png"
    driver.find_element(By.NAME, "user_password").send_keys("admin")
    driver.save_screenshot(screenshot_path)
    steps.append((detalle, screenshot_path))

    # Paso 3
    detalle = "Se hizo click en 'Iniciar Sesión'."
    driver.find_element(By.ID, "submit").click()
    time.sleep(2)
    screenshot_path = f"../evidencia/screenshots/step_submit_{int(time.time())}.png"
    driver.save_screenshot(screenshot_path)
    steps.append((detalle, screenshot_path))

    # Paso 4
    if "stock.php" in driver.current_url:
        detalle = "Login exitoso: redirigió a stock.php."
    else:
        detalle = f"Login fallido: URL actual es {driver.current_url}\n"
        try:
            alert = driver.find_element(By.CLASS_NAME, "alert-danger")
            detalle += f"Mensaje de error: {alert.text}"
        except NoSuchElementException:
            detalle += "No se encontró mensaje de error."

        status = "FAILED"
        color_status = (255, 0, 0)

    screenshot_path = f"../evidencia/screenshots/step_resultado_{int(time.time())}.png"
    driver.save_screenshot(screenshot_path)
    steps.append((detalle, screenshot_path))

except Exception as e:
    status = "FAILED"
    color_status = (255, 0, 0)
    detalle = f"Excepción en el flujo: {type(e).__name__} - {e}"
    screenshot_path = f"../evidencia/screenshots/step_excepcion_{int(time.time())}_status.png"
    driver.save_screenshot(screenshot_path)
    steps.append((detalle, screenshot_path))
finally:
    driver.quit()

pdf_path = f"../evidencia/pdfs/evidencia_login_{status}.pdf"


generar_pdf_completo(step_name, status, color_status, now, steps, pdf_path)
