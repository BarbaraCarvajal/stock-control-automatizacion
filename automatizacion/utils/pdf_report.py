from fpdf import FPDF

def generar_pdf_completo(step_name, status, color_status, now, steps, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # === PRIMERA PAGINA GENERAL ===
    pdf.add_page()
    pdf.set_font("Helvetica", size=20)
    pdf.cell(0, 20, "Evidencia de Automatización", ln=True, align='C')
    pdf.set_font("Helvetica", size=14)
    pdf.cell(0, 10, f"Fecha: {now}", ln=True, align='C')
    pdf.ln(20)

    pdf.set_font("Helvetica", size=16)
    pdf.cell(0, 10, "Proyecto:", ln=True)
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, "Automatización del Registro de Producto", ln=True)
    pdf.ln(10)

    pdf.set_font("Helvetica", size=16)
    pdf.cell(0, 10, "Descripción:", ln=True)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8,
        "Este documento contiene la evidencia visual paso a paso del flujo automatizado "
        "para registrar un producto en el sistema local, con capturas de pantalla y detalles "
        "de cada acción realizada."
    )

    pdf.ln(10)
    pdf.set_font("Helvetica", size=14)
    pdf.set_text_color(*color_status)
    pdf.cell(0, 10, f"Estado final del flujo: {status}", ln=True)
    pdf.set_text_color(0, 0, 0)

    # === PASOS ===
    for idx, (detalle, screenshot_path) in enumerate(steps, start=1):
        pdf.add_page()
        pdf.set_line_width(1)
        pdf.set_draw_color(*color_status)
        pdf.rect(10, 10, 190, 277)

        # Si el test falló, en la primera página de pasos muestra aviso
        if idx == 1 and status == "FAILED":
            pdf.set_font("Helvetica", size=18)
            pdf.set_text_color(255, 0, 0)
            pdf.cell(0, 15, "El test falló en este paso:", ln=True, align='C')
            pdf.ln(5)
            pdf.set_text_color(0, 0, 0)

        pdf.set_font("Helvetica", size=16)
        pdf.cell(0, 10, f"Paso {idx}", ln=True)
        pdf.ln(5)

        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 8, detalle)
        pdf.ln(5)

        try:
            pdf.image(screenshot_path, x=20, w=170)
        except:
            pdf.cell(0, 10, f"[No se pudo cargar imagen: {screenshot_path}]", ln=True)

    pdf.output(filename)
    print(f"✅ PDF generado: {filename}")
