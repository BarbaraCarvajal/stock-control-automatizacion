# 🚀 Automatización QA con Python + Selenium + Evidencia PDF

Este proyecto contiene scripts de automatización de pruebas para un sistema web de inventario.  
Automatiza el flujo de login y registro de productos, generando un PDF con la evidencia visual paso a paso.

---

## ✨ ¿Qué hace este proyecto?

✅ Ejecuta pruebas automáticas con Selenium WebDriver.  
✅ Valida flujos críticos (login, alta de productos).  
✅ Toma capturas de pantalla en cada paso.  
✅ Genera un PDF consolidado con los pasos, sus descripciones y el estado final (`PASSED` o `FAILED`).

---

## ⚙ Requisitos

### 🐍 Python 3.8+
Debes tener `python` y `pip` disponibles en tu terminal (Windows, macOS o Linux).

Verifica con:

```bash
python --version
pip --version
```


### 📦 Dependencias Python

Instala las dependencias del proyecto con: 
```
pip install selenium fpdf2
```


### 🌐 Google Chrome

Debes tener Google Chrome instalado (en Windows, macOS o Linux).


### 🚀 Cómo ejecutar las pruebas

Las pruebas están en el directorio tests/.

## 🧪 Lista de casos disponibles

### 🔐 Login

### ✅ F01 Validar que el sistema permita iniciar sesión con credenciales válidas

```
python automatizacion/tests/F01_validar_que_el_sistema_permita_iniciar_sesión_con_credenciales_validas.py
```

### ❌ F02 Validar que el sistema no permita iniciar sesión con credenciales inválidas

```
python automatizacion/tests/F02_validar_que_el_sistema_no_permita_iniciar_sesión_con_credenciales_invalidas.py
```

### 📦 Registro de productos

### ✅ F03 Validar que se permita registrar un producto con todos los campos válidos

```
python automatizacion/tests/F03_validar_que_se_permita_registrar_un_producto_con_todos_los_campos_validos.py
```

### ❌ F04 Validar que el sistema no permita registrar un producto si faltan campos obligatorios
```
python automatizacion/tests/F04_validar_que_el_sistema_no_permita_registrar_un_producto_si_faltan_campos_obligatorios.py
```

### 🔍 Filtros

### ✅ F07 Validar que el sistema filtra por nombre, código o categoría
```
python automatizacion/tests/F07_Validar_que_el_sistema_filtra_por_nombre_codigo_o_categoria.py
```

### ✏️ Edición

### ✅ F13 Validar que se permita editar el nombre y la descripción de una categoría existente
```
python automatizacion/tests/F13_Validar_que_se_permita_editar_el_nombre_y_la_descripción_de_una_categoría_existente.py
```

### ✅ F16 Validar que se permita editar el nombre de un producto existente
```
python automatizacion/tests/F16_Validar_que_se_permita_editar_el_nombre_de_un_producto_existente.py
```

---

## 📂 Evidencias
Cada prueba genera un PDF en la carpeta evidencia/pdfs/ con:

✅ Screenshots paso a paso
✅ Descripciones automáticas
✅ Estado final (PASSED o FAILED)
