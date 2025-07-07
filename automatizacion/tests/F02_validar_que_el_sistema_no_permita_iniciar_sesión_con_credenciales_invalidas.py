import glob
import sys
import os
import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.pdf_report import generar_pdf_completo
from utils.metodos_genericos import enmarcar_elemento, desmarcar_elemento
from config_rutas import SCREENSHOTS_DIR, PDFS_DIR

def run_test():
    # Limpia screenshots antes de correr
    for file in glob.glob(os.path.join(SCREENSHOTS_DIR, "*.png")):
        os.remove(file)

    step_name = "Flujo Login en sistema local con credenciales inválidas"
    status = "PASSED"
    color_status = (0, 128, 0)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    steps = []

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("http://localhost/control/login.php")

        # Paso 1: Usuario incorrecto
        user_input = driver.find_element(By.NAME, "user_name")
        enmarcar_elemento(driver, user_input)
        time.sleep(0.2)
        user_input.send_keys("a2dmin")
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_usuario_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, user_input)
        steps.append(("Usuario inválido ingresado correctamente.", screenshot))

        # Paso 2: Contraseña
        pass_input = driver.find_element(By.NAME, "user_password")
        enmarcar_elemento(driver, pass_input)
        time.sleep(0.2)
        pass_input.send_keys("admin")
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_password_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, pass_input)
        steps.append(("Contraseña ingresada correctamente.", screenshot))

        # Paso 3: Botón
        boton_login = driver.find_element(By.ID, "submit")
        enmarcar_elemento(driver, boton_login)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_submit_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, boton_login)
        boton_login.click()
        steps.append(("Se hizo click en 'Iniciar Sesión'.", screenshot))

        # Paso 4: Resultado esperado es que NO loguee
        time.sleep(2)
        if "stock.php" in driver.current_url:
            # Error: se logró loguear con credenciales inválidas
            detalle = "⚠ ERROR: Login NO debería haberse completado, pero redirigió a stock.php."
            status = "FAILED"
            color_status = (255, 0, 0)
        else:
            detalle = f"Login correctamente rechazado. URL actual: {driver.current_url}"
            try:
                alert = driver.find_element(By.CLASS_NAME, "alert-danger")
                detalle += f" | Mensaje mostrado: {alert.text}"
            except NoSuchElementException:
                detalle += " | Sin mensaje de error visible, pero no redirigió."

        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_resultado_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append((detalle, screenshot))

    except Exception as e:
        status = "FAILED"
        color_status = (255, 0, 0)
        detalle = f"Excepción en el flujo: {type(e).__name__} - {e}"
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_excepcion_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append((detalle, screenshot))
    finally:
        driver.quit()
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        pdf_path = os.path.join(PDFS_DIR, f"{file_name}_{status}.pdf")
        generar_pdf_completo(
            step_name,
            "Este test valida que el sistema NO permita iniciar sesión si las credenciales son inválidas.",
            status, color_status, now, steps, pdf_path
        )

if __name__ == "__main__":
    run_test()
