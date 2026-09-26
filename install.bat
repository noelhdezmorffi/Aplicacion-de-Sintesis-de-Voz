@echo off
REM Script de instalación para Windows
REM Instala todas las dependencias necesarias

chcp 65001 >nul
color 0A
cls

echo ==========================================
echo   Instalador - Lector IA v1.0.0
echo ==========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [✗] ERROR: Python no está instalado o no está en el PATH
    echo.
    echo SOLUCIÓN:
    echo 1. Descarga Python desde: https://www.python.org/downloads/
    echo 2. IMPORTANTE: Marca "Add Python to PATH" durante la instalación
    echo 3. Instala la versión 3.8 o superior
    echo 4. Reinicia esta consola
    echo 5. Ejecuta este instalador de nuevo
    echo.
    echo Si ya instalaste Python:
    echo - Asegúrate de haber marcado "Add Python to PATH"
    echo - Reinicia tu computadora
    echo - Ejecuta este instalador de nuevo
    echo.
    pause
    exit /b 1
)

python --version
echo [✓] Python detectado
echo.

REM Crear entorno virtual
echo [*] Creando entorno virtual...
if exist venv (
    echo [!] Entorno virtual ya existe, se usará el existente
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [✗] Error al crear entorno virtual
        pause
        exit /b 1
    )
)

echo [*] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [*] Instalando dependencias (esto puede tomar varios minutos)...
echo.
pip install --upgrade pip
if errorlevel 1 (
    echo [✗] Error al actualizar pip
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo [✗] Error al instalar dependencias
    echo.
    echo Intenta ejecutar manualmente:
    echo pip install PyQt5 pyttsx3 PyPDF2 python-docx Pillow pytesseract mss
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo [✓] ¡Instalación completada!
echo ==========================================
echo.
echo SIGUIENTE PASO - Configurar Tesseract OCR:
echo.
echo 1. Descarga desde: https://github.com/UB-Mannheim/tesseract/wiki
echo 2. Ejecuta el instalador (TesseractOCR-v5.x.exe)
echo 3. Instala en: C:\Program Files\Tesseract-OCR
echo 4. Deja las opciones por defecto
echo.
echo PARA EJECUTAR LA APLICACIÓN:
echo.
echo Opción 1: Haz doble clic en "run.bat"
echo Opción 2: En esta consola, ejecuta: run.bat
echo.
pause
