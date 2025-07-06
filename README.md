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

### 🔐 Prueba de login

```
python tests/test_login.py

```

### 📦 Prueba de registro de producto

```
python tests/test_registro_producto.py

```



