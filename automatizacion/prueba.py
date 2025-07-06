from selenium import webdriver
from selenium.webdriver.common.by import By
from fpdf import FPDF
import time
from datetime import datetime

# Datos del test
step_name = "Login en sistema local"
status = "PASSED"
color_status = (0, 128, 0)
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Selenium
driver = webdriver.Chrome()
driver.get("http://localhost/control/login.php")
try:
    driver.find_element(By.NAME, "user_name").send_keys("admin")
    driver.find_element(By.NAME, "user_password").send_keys("admin")
    driver.find_element(By.ID, "submit").click()
    time.sleep(2)
    screenshot_path = "evidencia_login.png"
    driver.save_screenshot(screenshot_path)
except Exception as e:
    status = "FAILED"
    color_status = (255, 0, 0)
finally:
    driver.quit()

# PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", "B", 16)

# Dibujar recuadro con color
pdf.set_line_width(1)
pdf.set_draw_color(*color_status)  # cambia el color del borde
pdf.rect(10, 10, 190, 277)

# Título centrado
pdf.cell(200, 10, "Reporte de Automatización", ln=True, align='C')
pdf.set_font("Helvetica", size=12)
pdf.cell(200, 10, f"Fecha: {now}", ln=True, align='C')
pdf.ln(10)

# Nombre del step
pdf.set_font("Helvetica", "B", 14)
pdf.cell(40, 10, "Step:")
pdf.set_font("Helvetica", size=12)
pdf.cell(100, 10, step_name, ln=True)

# Estado con color
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(*color_status)
pdf.cell(40, 10, "Estado:")
pdf.cell(100, 10, status, ln=True)
pdf.set_text_color(0, 0, 0)
pdf.ln(10)

# Imagen
pdf.image(screenshot_path, x=30, w=150)

# Guardar PDF
pdf.output("evidencia_login_recuadro_color.pdf")
print("✅ PDF con recuadro coloreado generado: evidencia_login_recuadro_color.pdf")
