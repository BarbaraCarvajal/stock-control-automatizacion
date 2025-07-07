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

    steps = []
    status = "PASSED"
    color_status = (0, 128, 0)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    codigo_random = f"SEL{random.randint(0,999):03}"

    try:
        # 1. Login
        driver.get("http://localhost/Control/login.php")
        user_input = driver.find_element(By.NAME, "user_name")
        enmarcar_elemento(driver, user_input)
        time.sleep(0.2)
        user_input.send_keys("admin")
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_user_input_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, user_input)

        pass_input = driver.find_element(By.NAME, "user_password")
        enmarcar_elemento(driver, pass_input)
        time.sleep(0.2)
        pass_input.send_keys("admin")
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_pass_input_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, pass_input)

        boton_login = driver.find_element(By.ID, "submit")
        enmarcar_elemento(driver, boton_login)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_login_btn_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, boton_login)
        boton_login.click()

        wait.until(EC.url_contains("stock.php"))
        detalle = "Login exitoso redirigido a stock.php"
        steps.append((detalle, screenshot))

        # 2. Inventario
        titulo = driver.find_element(By.XPATH, "//h4[contains(text(),'Consultar inventario')]")
        enmarcar_elemento(driver, titulo)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_titulo_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, titulo)
        steps.append(("Título 'Consultar inventario' visible.", screenshot))

        # 3. Modal nuevo producto
        boton_agregar = driver.find_element(By.XPATH, "//button[contains(text(),'Agregar')]")
        enmarcar_elemento(driver, boton_agregar)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_btn_agregar_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, boton_agregar)
        boton_agregar.click()

        wait.until(EC.visibility_of_element_located((By.ID, "nuevoProducto")))
        detalle = "Modal para nuevo producto abierto."
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_modal_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append((detalle, screenshot))

        # 4. Formulario
        codigo_input = driver.find_element(By.ID, "codigo")
        enmarcar_elemento(driver, codigo_input)
        time.sleep(0.2)
        codigo_input.send_keys(codigo_random)
        desmarcar_elemento(driver, codigo_input)

        nombre_input = driver.find_element(By.ID, "nombre")
        enmarcar_elemento(driver, nombre_input)
        time.sleep(0.2)
        nombre_input.send_keys("Taladro 2000xl")
        desmarcar_elemento(driver, nombre_input)

        select_categoria = Select(driver.find_element(By.ID, "categoria"))
        select_categoria.select_by_index(2)

        precio_input = driver.find_element(By.ID, "precio")
        enmarcar_elemento(driver, precio_input)
        time.sleep(0.2)
        precio_input.send_keys("150")
        desmarcar_elemento(driver, precio_input)

        stock_input = driver.find_element(By.ID, "stock")
        enmarcar_elemento(driver, stock_input)
        time.sleep(0.2)
        stock_input.send_keys("500")
        desmarcar_elemento(driver, stock_input)

        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_formulario_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        steps.append((f"Formulario completado con código {codigo_random}.", screenshot))

        # 5. Guardar
        btn_guardar = driver.find_element(By.ID, "guardar_datos")
        enmarcar_elemento(driver, btn_guardar)
        time.sleep(0.2)
        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_guardar_{int(time.time())}.png")
        driver.save_screenshot(screenshot)
        desmarcar_elemento(driver, btn_guardar)
        btn_guardar.click()

        time.sleep(2)
        detalle = "Botón 'Guardar datos' presionado."
        steps.append((detalle, screenshot))

        # 6. Mensaje éxito
        try:
            mensaje = driver.find_element(By.XPATH, "//div[contains(@class,'alert-success')]")
            assert "Producto ha sido ingresado" in mensaje.text
            detalle = f"Producto ingresado exitosamente: {mensaje.text}"
        except NoSuchElementException:
            detalle = "No se encontró mensaje de éxito."
            status = "FAILED"
            color_status = (255, 0, 0)

        screenshot = os.path.join(SCREENSHOTS_DIR, f"step_mensaje_{int(time.time())}.png")
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
            "Flujo Registro Producto",
            "Este test valida que se pueda registrar un nuevo producto correctamente.",
            status, color_status, now, steps, pdf_path
        )

if __name__ == "__main__":
    run_test()
