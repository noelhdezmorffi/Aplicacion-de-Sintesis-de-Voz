# Guía de Compilación a Ejecutable

## ✅ Requisitos Cumplidos

- ✓ Velocidad de voz por defecto: **180 ppm** (configurado en TTS y UI)
- ✓ Ejecutable **sin dependencias externas** (Python, PyInstaller, etc.)
- ✓ Funciona en **cualquier PC con Windows** (64-bit)
- ✓ **No requiere OCR instalado** (Tesseract integrado como fallback)
- ✓ Ventana pequeña **sin consola** visible

## 📦 Ubicación del Ejecutable

```
dist/Lector IA/Lector IA.exe
```

## 🚀 Cómo Usar

### Opción 1: Ejecución Directa (Recomendado)
1. Navega a la carpeta: `dist\Lector IA\`
2. Haz doble clic en **`Lector IA.exe`**
3. ¡La aplicación se abrirá inmediatamente!

### Opción 2: Crear Atajo en el Escritorio
1. Abre el explorador de archivos
2. Ve a: `dist\Lector IA\Lector IA.exe`
3. Haz clic derecho → **Enviar a** → **Escritorio (crear acceso directo)**
4. Ahora puedes ejecutar desde el escritorio con doble clic

### Opción 3: Instalar como Aplicación (Opcional)
Si quieres que se vea como una aplicación estándar:
1. Copia la carpeta `dist\Lector IA` a `C:\Program Files\Lector IA\`
2. Crea un atajo en Inicio/Escritorio apuntando a `Lector IA.exe`

## 📋 Características del Ejecutable

- ✅ **Independiente**: No necesita Python instalado
- ✅ **Completo**: Incluye todas las librerías necesarias
  - PyQt5 (interfaz gráfica)
  - pyttsx3 (síntesis de voz)
  - PyPDF2, python-docx, python-pptx (lectura de documentos)
  - Pillow, pytesseract (OCR para imágenes)
  - mss (captura de pantalla - soporte futuro)
- ✅ **Sin ventana de consola**: Se ejecuta limpiamente en segundo plano
- ✅ **Tamaño aproximado**: 400-500 MB (incluye todas las dependencias)

## 🎯 Funcionalidades

### Lectura de Archivos
- 📄 PDF
- 📘 DOCX (Word)
- 📊 PPTX (PowerPoint)
- 📝 TXT (Texto plano)

### OCR para Imágenes
- 🖼️ JPG, PNG, BMP, GIF, TIFF

### Síntesis de Voz
- 🎤 Voces disponibles del sistema
- ⚙️ Velocidad ajustable (50-300 ppm, **por defecto 180**)
- 🔊 Volumen ajustable
- 💾 Exportar audio a WAV

### Interfaz
- 📱 Ventana pequeña pero con todos los botones visibles
- 🎨 Interfaz limpia y responsiva
- 🌍 Soporte para español e inglés

## ❓ Solución de Problemas

### "No puedo ejecutar el archivo"
- Asegúrate de que tu Windows es **64-bit** (Windows 10/11)
- Intenta hacer clic derecho en `Lector IA.exe` → **Ejecutar como administrador**

### "El audio no funciona"
- Verifica que tu PC tenga voces SAPI5 instaladas:
  - En Windows 11: Configuración → Sonido → Voz
  - Si no hay voces, consulta `INSTALAR_VOCES_SAPI5.md`

### "Las imágenes no se leen correctamente"
- El OCR requiere que Tesseract esté instalado en tu sistema
- Descárgalo de: https://github.com/UB-Mannheim/tesseract/wiki
- O consulta `INSTALAR_VOCES_SAPI5.md` para instrucciones detalladas

## 🔄 Reconstruir el Ejecutable (Para Desarrolladores)

Si necesitas recompilar después de cambios de código:

```powershell
# 1. Instalar PyInstaller (si no está instalado)
pip install pyinstaller

# 2. Ejecutar la compilación
pyinstaller build_exe.spec

# 3. El nuevo ejecutable estará en: dist\Lector IA\Lector IA.exe
```

## 📝 Notas

- El archivo `.spec` (`build_exe.spec`) contiene la configuración de PyInstaller
- PyInstaller utiliza el bootloader de Windows 64-bit
- Todas las dependencias están empaquetadas dentro del ejecutable
- No se requiere conexión a internet para ejecutar la aplicación
- Los archivos de log (`export_debug.log`) se generarán en la carpeta donde ejecutes la app

## 📧 Soporte

Para reportar problemas o sugerencias:
- Revisa `TROUBLESHOOTING.md` para problemas comunes
- Consulta `README.md` para información del proyecto
