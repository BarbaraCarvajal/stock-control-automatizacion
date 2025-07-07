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

    step_name = "Flujo Validar Restricción Registro Producto"
    status = "PASSED"
    color_status = (0, 128, 0)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    steps = []

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    codigo_random = f"SEL{random.randint(0, 999):03}"

    try:
        # 1. Login
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

        # 2. Abrir modal para nuevo producto
        boton_agregar = driver.find_element(By.XPATH, "//button[contains(text(),'Agregar')]")
        enmarcar_elemento(driver, boton_agregar)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_open_modal_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, boton_agregar)
        boton_agregar.click()

        wait.until(EC.visibility_of_element_located((By.ID, "nuevoProducto")))
        steps.append(("Modal para nuevo producto abierto.", screenshot))

        # 3. Completar solo algunos campos y dejar el stock vacío
        input_codigo = driver.find_element(By.ID, "codigo")
        enmarcar_elemento(driver, input_codigo)
        input_codigo.send_keys(codigo_random)
        desmarcar_elemento(driver, input_codigo)

        input_nombre = driver.find_element(By.ID, "nombre")
        enmarcar_elemento(driver, input_nombre)
        input_nombre.send_keys("Taladro sin stock")
        desmarcar_elemento(driver, input_nombre)

        select_categoria = Select(driver.find_element(By.ID, "categoria"))
        select_categoria.select_by_index(2)

        input_precio = driver.find_element(By.ID, "precio")
        enmarcar_elemento(driver, input_precio)
        input_precio.send_keys("150")
        desmarcar_elemento(driver, input_precio)

        # NOTA: No llenamos el stock

        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_formulario_incompleto_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append(("Formulario incompleto (sin stock) listo para enviar.", screenshot))

        # 4. Intentar guardar
        btn_guardar = driver.find_element(By.ID, "guardar_datos")
        enmarcar_elemento(driver, btn_guardar)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_guardar_click_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, btn_guardar)
        btn_guardar.click()
        steps.append(("Botón 'Guardar datos' presionado con formulario incompleto.", screenshot))

        # 5. Validar restricción
        time.sleep(2)  # dar tiempo al ajax
        try:
            mensaje = driver.find_element(By.XPATH, "//div[contains(@class,'alert-danger')]")
            detalle = f"Validación correcta: el sistema mostró error -> {mensaje.text}"
        except NoSuchElementException:
            # Verificar si el producto sin stock se agregó, lo cual sería incorrecto
            html = driver.page_source
            if codigo_random in html:
                detalle = f"Producto con datos incompletos fue agregado ERRONEAMENTE (codigo {codigo_random})."
                status = "FAILED"
                color_status = (255, 0, 0)
            else:
                detalle = "No se agregó el producto con datos incompletos, validación correcta."

        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_validacion_{int(time.time())}.png")
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
            step_name,
            "Este test valida que el sistema NO permita registrar un producto si no se completan todos los campos requeridos.",
            status, color_status, now, steps, pdf_path
        )

if __name__ == "__main__":
    run_test()
