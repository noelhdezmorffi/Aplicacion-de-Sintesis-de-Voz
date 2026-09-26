# 🔧 Solución de Problemas - Lector IA

## 🆘 Problemas Comunes y Soluciones

### 1. Error: "pytesseract.TesseractNotFoundError"

**Problema**: La aplicación no puede encontrar Tesseract OCR

**Soluciones**:

#### Windows
```powershell
# Opción 1: Descargar e instalar Tesseract
# Visita: https://github.com/UB-Mannheim/tesseract/wiki
# Descarga TesseractOCR-v5.x.exe
# Instala en C:\Program Files\Tesseract-OCR

# Opción 2: Ejecutar el script de configuración
python setup_tesseract.py

# Opción 3: Configuración manual
# Edita src/modules/text_extractor.py
# Agrega después del import:
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```

#### macOS
```bash
brew install tesseract
```

---

### 2. Error: "ModuleNotFoundError: No module named 'PyQt5'"

**Problema**: Las dependencias no están instaladas

**Solución**:
```powershell
# Windows
pip install -r requirements.txt

# O instalar manualmente:
pip install PyQt5 pyttsx3 PyPDF2 python-docx Pillow pytesseract python-pptx mss
```

```bash
# Linux/Mac
pip3 install -r requirements.txt
```

---

### 3. La aplicación se abre pero no hay sonido

**Problema**: El motor de síntesis de voz no funciona

**Soluciones**:

#### Windows
- Windows incluye el motor SAPI5 por defecto
- Verifica que los altavoces estén encendidos
- Prueba aumentar el volumen en la aplicación

#### Linux
```bash
sudo apt-get install espeak espeak-ng
```

#### macOS
- macOS incluye el motor de síntesis por defecto
- Verifica que los altavoces estén encendidos

---

### 4. No se extrae texto de imágenes

**Problema**: El OCR no reconoce el texto en imágenes

**Posibles causas y soluciones**:

1. **Tesseract no está instalado**
   - Ver problema #1 arriba

2. **Imagen de mala calidad**
   - El OCR funciona mejor con imágenes claras de alta resolución
   - Prueba con una imagen de mejor calidad

3. **Idioma no configurado**
   - Por defecto se usa "spa+eng" (Español + Inglés)
   - Para agregar más idiomas, edita `src/modules/text_extractor.py`
   - Cambia la línea: `pytesseract.image_to_string(image, lang='spa+eng')`
   - Idiomas: fra (Francés), deu (Alemán), por (Portugués), etc.

4. **Tesseract no encuentra los archivos de idioma**
   - Windows: Reinstala Tesseract seleccionando los idiomas
   - Linux: `sudo apt-get install tesseract-ocr-all`

---

### 5. Error: "AttributeError: 'NoneType' object has no attribute..."

**Problema**: Error general de atributos

**Solución**:
```powershell
# Ejecuta el script de pruebas para diagnosticar
python test.py

# Esto te mostrará qué módulo está fallando
```

---

### 6. PyQt5 no funciona en Linux

**Problema**: "ImportError: Could not find the Qt platform plugin"

**Solución** (Ubuntu/Debian):
```bash
sudo apt-get install python3-pyqt5
sudo apt-get install libqt5gui5
```

---

### 7. La aplicación se congela

**Problema**: La interfaz se congela durante la lectura

**Solución**:
- Es normal que se congele brevemente mientras se genera la voz
- En versiones futuras usaremos más hilos para mejorar la responsividad
- Paciencia: la síntesis de voz toma tiempo

---

### 8. Error: "File is too large"

**Problema**: El archivo es demasiado grande (>100 MB)

**Solución**:
- Divide el archivo en partes más pequeñas
- O aumenta el límite en `src/config.py`:
```python
MAX_FILE_SIZE = 200  # Cambiar a 200 MB
```

---

### 9. Error de Encoding en archivos de texto

**Problema**: "UnicodeDecodeError" al leer archivos .txt

**Causa**: El archivo usa un encoding diferente

**Solución**:
- El código intenta UTF-8 primero, luego Latin-1
- Si aún así falla, convierte el archivo:
```powershell
# Windows PowerShell
Get-Content archivo.txt | Out-File archivo_utf8.txt -Encoding UTF8
```

```bash
# Linux
iconv -f ISO-8859-1 -t UTF-8 archivo.txt > archivo_utf8.txt
```

---

### 10. Error al leer archivos Word protegidos

**Problema**: No se pueden leer documentos Word con contraseña

**Solución**:
- Abre el documento en Word
- Guarda una copia sin protección
- Usa la copia en Lector IA

---

## 🧪 Verificación del Sistema

### Script de Pruebas
```powershell
python test.py
```

Este script verifica:
- ✓ Importación de módulos
- ✓ Disponibilidad de voces
- ✓ Formatos soportados
- ✓ Configuración general

### Ejemplo de Uso
```powershell
python examples.py
```

Ejecuta ejemplos prácticos de los módulos.

---

## 📋 Checklist de Instalación

Antes de reportar un error, verifica:

- [ ] Python 3.8+ instalado: `python --version`
- [ ] Tesseract instalado: `tesseract --version`
- [ ] Entorno virtual creado: `venv` existe
- [ ] Dependencias instaladas: `pip list | grep -E "(PyQt5|pyttsx3|pytesseract)"`
- [ ] Script de pruebas funciona: `python test.py`

---

## 🚨 Reportar Errores

Si encuentras un error que no está aquí:

1. **Ejecuta el script de pruebas**:
   ```powershell
   python test.py
   ```

2. **Copia el error completo** (incluyendo el stack trace)

3. **Abre un issue** en el repositorio con:
   - Tu sistema operativo y versión
   - Versión de Python
   - El error exacto
   - Pasos para reproducir el error

---

## 📞 Soporte

- 📖 Lee la documentación completa: `README.md`
- 🚀 Guía rápida: `QUICKSTART.md`
- 📁 Estructura del proyecto: `PROJECT_STRUCTURE.md`
- 📝 Historial de cambios: `CHANGELOG.md`

---

**¡Esperamos ayudarte pronto!** 😊
