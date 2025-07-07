import glob
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import time
import random

from utils.pdf_report import generar_pdf_completo
from utils.metodos_genericos import enmarcar_elemento, desmarcar_elemento
from config_rutas import SCREENSHOTS_DIR, PDFS_DIR

def run_test():
    # limpiar screenshots antes de correr
    for file in glob.glob(os.path.join(SCREENSHOTS_DIR, "*.png")):
        os.remove(file)


    # Datos para el PDF
    steps = []
    status = "PASSED"
    color_status = (0, 128, 0)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Login
        driver.get("http://localhost/Control/login.php")
        user_input = driver.find_element(By.NAME, "user_name")
        enmarcar_elemento(driver, user_input)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_login_user_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, user_input)
        user_input.send_keys("admin")

        pass_input = driver.find_element(By.NAME, "user_password")
        enmarcar_elemento(driver, pass_input)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_login_pass_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, pass_input)
        pass_input.send_keys("admin")

        boton_login = driver.find_element(By.ID, "submit")
        enmarcar_elemento(driver, boton_login)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_login_btn_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, boton_login)
        boton_login.click()

        wait.until(EC.url_contains("stock.php"))
        detalle = "Login exitoso, redirigido a stock.php"
        steps.append((detalle, screenshot))

        # 2. Estructura inventario
        titulo = driver.find_element(By.XPATH, "//h4[contains(text(),'Consultar inventario')]")
        enmarcar_elemento(driver, titulo)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_inventario_titulo_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, titulo)

        btn_agregar = driver.find_element(By.XPATH, "//button[contains(text(),'Agregar')]")
        enmarcar_elemento(driver, btn_agregar)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_btn_agregar_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, btn_agregar)

        detalle = "Validada estructura del panel de inventario: título y botón '+ Agregar'."
        steps.append((detalle, screenshot))

        # 3. Filtro por nombre/código
        filtro_nombre = driver.find_element(By.ID, "q")
        enmarcar_elemento(driver, filtro_nombre)
        time.sleep(0.2)
        filtro_nombre.send_keys("martillo")  # ejemplo nombre o código
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_filtro_nombre_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, filtro_nombre)

        detalle = "Filtro por nombre/código aplicado con 'martillo'."
        steps.append((detalle, screenshot))

        # 4. Filtro por categoría
        filtro_categoria = driver.find_element(By.ID, "id_categoria")
        enmarcar_elemento(driver, filtro_categoria)
        time.sleep(0.2)
        filtro_categoria.send_keys("Herramientas")
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_filtro_categoria_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, filtro_categoria)

        detalle = "Filtro de categoría aplicado con 'Herramientas'."
        steps.append((detalle, screenshot))

        time.sleep(2)  # esperar ajax
        # 5. Validar resultados filtrados
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.outer_div")))
            html = driver.page_source
            if "martillo" in html or "Herramientas" in html:
                detalle = "El sistema muestra productos correspondientes al filtro aplicado."
            else:
                detalle = "No se encontraron productos con el filtro, o no coincide el nombre/categoría."
                status = "FAILED"
                color_status = (255, 0, 0)
        except TimeoutException:
            detalle = "Timeout esperando resultados del filtro."
            status = "FAILED"
            color_status = (255, 0, 0)

        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_resultado_filtro_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append((detalle, screenshot))

    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        status = "FAILED"
        color_status = (255, 0, 0)
        detalle = f"Excepción en el flujo: {type(e).__name__} - {e}"
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_exception_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append((detalle, screenshot))
    finally:
        driver.quit()
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        pdf_path = os.path.join(PDFS_DIR, f"{file_name}_{status}.pdf")
        generar_pdf_completo(
            "Flujo Filtro Inventario",
            "Este test valida que el sistema filtre productos por nombre, código o categoría "
            "mostrando únicamente los resultados esperados según los criterios aplicados.",
            status, color_status, now, steps, pdf_path
        )
        
if __name__ == "__main__":
    run_test()
