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
        # 1. Página de login
        driver.get("http://localhost/Control/login.php")
        detalle = "Página de login cargada."
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_login_page_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append((detalle, screenshot))

        # 2. Ingresar credenciales
        user_input = driver.find_element(By.NAME, "user_name")
        enmarcar_elemento(driver, user_input)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_user_input_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, user_input)
        user_input.send_keys("admin")

        pass_input = driver.find_element(By.NAME, "user_password")
        enmarcar_elemento(driver, pass_input)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_pass_input_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, pass_input)
        pass_input.send_keys("admin")

        detalle = "Credenciales ingresadas."
        steps.append((detalle, screenshot))

        # 3. Botón login
        boton_login = driver.find_element(By.ID, "submit")
        enmarcar_elemento(driver, boton_login)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_login_button_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, boton_login)
        boton_login.click()

        wait.until(EC.url_contains("stock.php"))
        detalle = "Login exitoso redirigido a stock.php"
        steps.append((detalle, screenshot))

        # 4. Ir a categorías
        categorias_link = driver.find_element(By.LINK_TEXT, "Categorías")
        enmarcar_elemento(driver, categorias_link)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_categorias_link_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, categorias_link)
        categorias_link.click()

        wait.until(EC.url_contains("categorias.php"))
        detalle = "Página de categorías cargada."
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_categorias_loaded_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append((detalle, screenshot))

        # 5. Validar título
        titulo = driver.find_element(By.XPATH, "//h4[contains(text(),'Buscar Categorías')]")
        enmarcar_elemento(driver, titulo)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_titulo_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, titulo)
        assert titulo.is_displayed()

        # 6. Validar botón nueva categoría
        btn_nueva = driver.find_element(By.XPATH, "//button[contains(text(),'Nueva Categoría')]")
        enmarcar_elemento(driver, btn_nueva)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_btn_nueva_categoria_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, btn_nueva)
        assert btn_nueva.is_displayed()

        detalle = "Título y botón '+ Nueva Categoría' validados."
        steps.append((detalle, screenshot))

        # 7. Click en lápiz para editar
        wait.until(EC.visibility_of_element_located((By.XPATH,"//a[contains(@data-target,'#myModal2')]"))) 
        lapiz = driver.find_element(By.XPATH, "//a[contains(@data-target,'#myModal2')]")
        enmarcar_elemento(driver, lapiz)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_lapiz_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, lapiz)
        lapiz.click()

        wait.until(EC.visibility_of_element_located((By.ID, "mod_nombre")))
        detalle = "Modal para editar categoría abierto."
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_modal_abierto_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append((detalle, screenshot))

        # 8. Editar campos
        nuevo_nombre = f"CategoriaEditada{random.randint(100,999)}"
        nueva_desc = f"Descripción editada {random.randint(100,999)}"

        input_nombre = driver.find_element(By.ID, "mod_nombre")
        enmarcar_elemento(driver, input_nombre)
        time.sleep(0.2)
        input_nombre.clear()
        input_nombre.send_keys(nuevo_nombre)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_edit_nombre_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, input_nombre)

        input_desc = driver.find_element(By.ID, "mod_descripcion")
        enmarcar_elemento(driver, input_desc)
        time.sleep(0.2)
        input_desc.clear()
        input_desc.send_keys(nueva_desc)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_edit_desc_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, input_desc)

        detalle = f"Campos editados con nombre '{nuevo_nombre}' y descripción '{nueva_desc}'."
        steps.append((detalle, screenshot))

        # 9. Click actualizar
        btn_actualizar = driver.find_element(By.ID, "actualizar_datos")
        enmarcar_elemento(driver, btn_actualizar)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_btn_actualizar_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, btn_actualizar)
        btn_actualizar.click()

        time.sleep(3)
        detalle = "Botón 'Actualizar datos' presionado."
        steps.append((detalle, screenshot))

        # 10. Validar en lista
        try:
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.outer_div"), nuevo_nombre))
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.outer_div"), nueva_desc))
            detalle = f"Categoría actualizada correctamente: {nuevo_nombre} - {nueva_desc}"
        except TimeoutException:
            detalle = "No se encontró la categoría actualizada."
            status = "FAILED"
            color_status = (255, 0, 0)

        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_validacion_final_{int(time.time())}.png")
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
            "Flujo Editar Categoría",
            "Este test valida que se pueda editar correctamente el nombre y descripción "
            "de una categoría existente en el sistema.",
            status, color_status, now, steps, pdf_path
        )
if __name__ == "__main__":
    run_test()

