import glob
import sys
import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.pdf_report import generar_pdf_completo
from utils.metodos_genericos import enmarcar_elemento, desmarcar_elemento
from config_rutas import SCREENSHOTS_DIR, PDFS_DIR

def run_test():
    for file in glob.glob(os.path.join(SCREENSHOTS_DIR, "*.png")):
        os.remove(file)

    step_name = "Flujo Editar Nombre Producto"
    status = "PASSED"
    color_status = (0, 128, 0)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    steps = []

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    nuevo_nombre = f"EditadoXYZ{random.randint(100,999)}"
    codigo_producto = "SEL516"  # Cambiar aquí el ID según el test

    try:
        # Login
        driver.get("http://localhost/Control/login.php")
        user_input = driver.find_element(By.NAME, "user_name")
        enmarcar_elemento(driver, user_input)
        user_input.send_keys("admin")
        desmarcar_elemento(driver, user_input)

        pass_input = driver.find_element(By.NAME, "user_password")
        enmarcar_elemento(driver, pass_input)
        pass_input.send_keys("admin")
        desmarcar_elemento(driver, pass_input)

        boton_login = driver.find_element(By.ID, "submit")
        enmarcar_elemento(driver, boton_login)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_login_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, boton_login)
        boton_login.click()

        wait.until(EC.url_contains("stock.php"))
        steps.append(("Login exitoso y redirigido a stock.php", screenshot))

        # Filtra por el ID
        filtro = driver.find_element(By.ID, "q")
        enmarcar_elemento(driver, filtro)
        filtro.clear()
        filtro.send_keys(codigo_producto)
        desmarcar_elemento(driver, filtro)
        time.sleep(1)

        # Espera que renderice productos
        wait.until(lambda d: len(d.find_elements(By.XPATH, "//img[contains(@src,'stock.png')]")) > 0)
        time.sleep(0.5)

        # Busca todos los contenedores de productos
        contenedor_correcto = None
        contenedores = driver.find_elements(By.XPATH, "//div[contains(@class,'row')]")

        for div in contenedores:
            try:
                # Busca que en el mismo contenedor exista el código exacto
                span_code = div.find_element(By.XPATH, f".//*[contains(text(),'{codigo_producto}')]")
                img_producto = div.find_element(By.XPATH, ".//img[contains(@src,'stock.png')]")
                
                if span_code and img_producto:
                    contenedor_correcto = div
                    break
            except NoSuchElementException:
                continue

        if not contenedor_correcto:
            screenshot = os.path.join(SCREENSHOTS_DIR, f"step_no_producto_{int(time.time())}.png")
            driver.save_screenshot(screenshot)
            steps.append((f"No se encontró producto con código '{codigo_producto}' junto a imagen.", screenshot))
            raise Exception(f"Producto con código '{codigo_producto}' no encontrado.")

        # Si encontró el contenedor correcto, hace click en la imagen de ese contenedor
        enmarcar_elemento(driver, img_producto)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_producto_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, img_producto)
        steps.append((f"Producto con código '{codigo_producto}' encontrado correctamente. Click para abrir detalle.", screenshot))
        img_producto.click()

        # Espera a producto.php
        wait.until(EC.url_contains("producto.php"))

        # Botón azul Editar
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Editar')]")))
        boton_editar = driver.find_element(By.XPATH, "//a[contains(.,'Editar')]")
        enmarcar_elemento(driver, boton_editar)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_btn_editar_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, boton_editar)
        boton_editar.click()
        steps.append(("Botón azul 'Editar' clickeado para abrir modal.", screenshot))

        # Editar nombre en modal
        wait.until(EC.visibility_of_element_located((By.ID, "mod_nombre")))
        input_nombre = driver.find_element(By.ID, "mod_nombre")
        enmarcar_elemento(driver, input_nombre)
        input_nombre.clear()
        input_nombre.send_keys(nuevo_nombre)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_edit_nombre_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, input_nombre)
        steps.append((f"Nombre editado a '{nuevo_nombre}'.", screenshot))

        # Guardar cambios
        btn_actualizar = driver.find_element(By.ID, "actualizar_datos")
        enmarcar_elemento(driver, btn_actualizar)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_guardar_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, btn_actualizar)
        btn_actualizar.click()
        steps.append(("Botón 'Actualizar datos' presionado.", screenshot))

        # Validar en outer_div
        time.sleep(4)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.outer_div")))
        html = driver.page_source
        if nuevo_nombre in html:
            detalle = f"Producto editado correctamente. Nuevo nombre: {nuevo_nombre}"
        else:
            detalle = f"El nombre editado '{nuevo_nombre}' no aparece en la lista."
            status = "FAILED"
            color_status = (255, 0, 0)

        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_validacion_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append((detalle, screenshot))

    except (TimeoutException, NoSuchElementException, AssertionError, Exception) as e:
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
            step_name,
            "Este test valida que se pueda editar el nombre de un producto filtrando por ID, asegurando contenedor exacto.",
            status, color_status, now, steps, pdf_path
        )

if __name__ == "__main__":
    run_test()
