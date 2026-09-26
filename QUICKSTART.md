# 🚀 Guía de Inicio Rápido - Lector IA

## ⚠️ REQUISITO PREVIO: Python

### Si ves el error: "Python no está instalado"

1. **Lee el archivo `PYTHON_SETUP.md`** en esta carpeta
2. Sigue las instrucciones para instalar Python
3. **IMPORTANTE**: Marca "Add Python to PATH" durante la instalación
4. Reinicia tu computadora
5. Vuelve a este archivo

---

## Instalación Rápida (Windows)

### Paso 1: Verificar Python
```powershell
# Abre PowerShell aquí
# Ejecuta:
check_python.bat

# Debería mostrar la versión de Python
```

### Paso 2: Descargar Tesseract OCR
1. Visita: https://github.com/UB-Mannheim/tesseract/wiki
2. Descarga el instalador para Windows (TesseractOCR-v5.x.exe)
3. Ejecuta el instalador
   - Acepta la licencia
   - Instala en la ubicación por defecto: `C:\Program Files\Tesseract-OCR`

### Paso 3: Instalar la Aplicación
1. Abre PowerShell en la carpeta del proyecto
2. Ejecuta: `.\install.bat`
3. Espera a que se instalen todas las dependencias (puede tomar varios minutos)

---

## Instalación Rápida (Linux - Ubuntu/Debian)

```bash
# Abrir terminal en la carpeta del proyecto
chmod +x install.sh
./install.sh
./run.sh
```

---

## Instalación Rápida (macOS)

```bash
# Requiere Homebrew
# Si no lo tienes: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

chmod +x install.sh
./install.sh
./run.sh
```

---

## Usar la Aplicación

### Leer un Archivo
1. Abre la pestaña "📄 Leer Archivo"
2. Haz clic en "📂 Abrir Archivo"
3. Selecciona un PDF, imagen, documento Word, etc.
4. El texto se extrae automáticamente
5. Haz clic en "▶️ Leer" para escuchar

### Leer la Pantalla
1. Abre la pestaña "🖥️ Leer Pantalla"
2. Haz clic en "📸 Capturar Pantalla"
3. Espera a que se realice el reconocimiento OCR
4. Haz clic en "▶️ Leer"

### Controlar la Lectura
- **▶️ Leer**: Comienza la reproducción
- **⏸️ Pausar**: Pausa en el punto actual
- **▶️ Reanudar**: Continúa desde donde se pausó
- **⏹️ Detener**: Detiene completamente

### Ajustar Configuración
1. Abre la pestaña "⚙️ Configuración"
2. **Velocidad**: Ajusta las palabras por minuto (50-300)
3. **Volumen**: Controla el nivel de sonido
4. **Voz**: Selecciona la voz preferida

---

## Archivos Soportados

### 📄 Documentos
- `.pdf` - Archivos PDF
- `.doc`, `.docx` - Documentos Word
- `.pptx` - Presentaciones PowerPoint
- `.txt` - Archivos de texto plano

### 🖼️ Imágenes
- `.jpg`, `.jpeg` - JPEG
- `.png` - PNG
- `.bmp` - BMP
- `.tiff`, `.tif` - TIFF
- `.gif` - GIF

---

## Solución de Problemas

### "No se puede encontrar Tesseract"
1. Descarga desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Instala en: `C:\Program Files\Tesseract-OCR`
3. Reinicia la aplicación

### "No se extrae texto de imágenes"
- Verifica que Tesseract esté instalado
- Intenta con una imagen con texto impreso claro
- El OCR funciona mejor con imágenes de alta resolución

### "La aplicación se cierra"
1. Abre PowerShell
2. Navega a la carpeta del proyecto
3. Activa el entorno: `.\venv\Scripts\activate`
4. Ejecuta: `python main.py`
5. Verifica los mensajes de error

### "Error de PyQt5"
En Linux: `sudo apt-get install python3-pyqt5`

### "La voz no funciona"
- Windows: Debería funcionar por defecto
- Linux: `sudo apt-get install espeak espeak-ng`
- macOS: Debería funcionar por defecto

---

## Atajos Útiles

| Acción | Atajo |
|--------|-------|
| Abrir archivo | Ctrl+O |
| Reproducir | Espacio |
| Pausar | Espacio |
| Detener | Escape |
| Aumentar velocidad | Ctrl+↑ |
| Disminuir velocidad | Ctrl+↓ |

---

## Preguntas Frecuentes

**¿Funciona sin internet?**
Sí, funciona completamente offline después de la instalación.

**¿Cuál es el tamaño máximo de archivo?**
Máximo 100 MB por archivo.

**¿Cuántos idiomas soporta?**
Español, Inglés, Francés y Alemán por defecto. Puedes agregar más en la configuración.

**¿Puedo cambiar la velocidad mientras lee?**
No durante la reproducción, pero puedes pausar y reanudar.

**¿Es gratuito?**
Sí, es software de código abierto.

---

## Contacto y Soporte

Para reportar problemas o sugerencias, abre un issue en el repositorio.

---

**¡Disfrutá leyendo!** 📖
