from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import os
import time
import sys
import random


# Para importar el generar_pdf_completo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.pdf_report import generar_pdf_completo

# Datos para el PDF
steps = []
status = "PASSED"
color_status = (0, 128, 0)
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
filename = f"../evidencia/pdfs/evidencia_registro_producto_{status}.pdf"

# Selenium
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

codigo_random = f"SEL{random.randint(0, 999):03}"


try:
    # 1. Página de login
    driver.get("http://localhost/Control/login.php")
    detalle = "Página de login cargada."
    screenshot = f"../evidencia/screenshots/step_login_page_{int(time.time())}.png"
    driver.save_screenshot(screenshot)
    steps.append((detalle, screenshot))

    # 2. Ingresar credenciales
    driver.find_element(By.NAME, "user_name").send_keys("admin")
    driver.find_element(By.NAME, "user_password").send_keys("admin")
    detalle = "Credenciales ingresadas en el formulario de login."
    screenshot = f"../evidencia/screenshots/step_credentials_{int(time.time())}.png"
    driver.save_screenshot(screenshot)
    steps.append((detalle, screenshot))

    # 3. Hacer clic en login
    driver.find_element(By.ID, "submit").click()
    wait.until(EC.url_contains("stock.php"))
    detalle = "Login exitoso y redirigido a stock.php"
    screenshot = f"../evidencia/screenshots/step_login_success_{int(time.time())}.png"
    driver.save_screenshot(screenshot)
    steps.append((detalle, screenshot))
    
    # 4. Validar título
    titulo = driver.find_element(By.XPATH, "//h4[contains(text(),'Consultar inventario')]")
    assert titulo.is_displayed()
    detalle = "Página de inventario con título 'Consultar inventario' visible."
    screenshot = f"../evidencia/screenshots/step_titulo_{int(time.time())}.png"
    driver.save_screenshot(screenshot)
    steps.append((detalle, screenshot))
    
    # 5. Abrir modal
    boton_agregar = driver.find_element(By.XPATH, "//button[contains(text(),'Agregar')]")
    boton_agregar.click()
    wait.until(EC.visibility_of_element_located((By.ID, "nuevoProducto")))
    detalle = "Modal para nuevo producto abierto."
    screenshot = f"../evidencia/screenshots/step_modal_{int(time.time())}.png"
    driver.save_screenshot(screenshot)
    steps.append((detalle, screenshot))

    
    # 6. Completar formulario
    driver.find_element(By.ID, "codigo").send_keys(codigo_random)
    driver.find_element(By.ID, "nombre").send_keys("Taladro 2000xl")
    select_categoria = Select(driver.find_element(By.ID, "categoria"))
    select_categoria.select_by_index(2)
    driver.find_element(By.ID, "precio").send_keys("150")
    driver.find_element(By.ID, "stock").send_keys("500")
    detalle = "Formulario completado con nuevo producto."
    screenshot = f"../evidencia/screenshots/step_formulario_{int(time.time())}.png"
    driver.save_screenshot(screenshot)
    steps.append((detalle, screenshot))
    
    # 7. Guardar datos
    driver.find_element(By.ID, "guardar_datos").click()
    time.sleep(2)  # pequeño tiempo para ajax
    detalle = "Botón 'Guardar datos' presionado."
    screenshot = f"../evidencia/screenshots/step_guardar_{int(time.time())}.png"
    driver.save_screenshot(screenshot)
    steps.append((detalle, screenshot))

    # 8. Validar mensaje de éxito
    try:
        mensaje = driver.find_element(By.XPATH, "//div[contains(@class,'alert-success')]")
        assert "Producto ha sido ingresado" in mensaje.text
        detalle = f"Producto ingresado exitosamente. ¡Bien hecho! {mensaje.text}"
    except NoSuchElementException:
        detalle = "No se encontró mensaje de éxito. Podría no haberse agregado el producto."
        status = "FAILED"
        color_status = (255, 0, 0)
    
    screenshot = f"../evidencia/screenshots/step_mensaje_{int(time.time())}.png"
    driver.save_screenshot(screenshot)
    steps.append((detalle, screenshot))

except (TimeoutException, NoSuchElementException, AssertionError) as e:
    status = "FAILED"
    color_status = (255, 0, 0)
    detalle = f"Excepción en el flujo: {type(e).__name__} - {e}"
    screenshot = f"../evidencia/screenshots/step_exception_{int(time.time())}.png"
    driver.save_screenshot(screenshot)
    steps.append((detalle, screenshot))
finally:
    driver.quit()
    filename = f"../evidencia/pdfs/evidencia_registro_producto_{status}.pdf"
    generar_pdf_completo("Flujo Registro Producto", status, color_status, now, steps, filename)
