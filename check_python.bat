@echo off
REM Verificador previo de Python
REM Ejecuta esto ANTES de install.bat

chcp 65001 >nul
color 0E
cls

echo.
echo ==========================================
echo   VERIFICADOR DE PYTHON
echo ==========================================
echo.

REM Buscar Python en el PATH
where python >nul 2>&1
if errorlevel 1 (
    echo [✗] Python NO se encontró en el PATH
    goto notsinstalled
) else (
    echo [✓] Python encontrado en el PATH
    python --version
    echo.
    goto installed
)

:notinstalled
echo.
echo ¿Qué hacer?
echo.
echo 1. DESCARGA Python desde: https://www.python.org/downloads/
echo 2. EJECUTA el instalador
echo 3. *** IMPORTANTE: Marca la opción "Add Python to PATH" ***
echo 4. REINICIA tu computadora después de instalar
echo 5. Abre una NUEVA consola (PowerShell/CMD)
echo 6. EJECUTA este script nuevamente
echo.
echo Si ya instalaste Python:
echo - Marca "Modify installation"
echo - Selecciona "Add Python to PATH"
echo - Reinicia tu computadora
echo.
pause
exit /b 1

:installed
echo [✓] ¡Python está listo!
echo.
echo Ahora ejecuta: install.bat
echo.
pause
exit /b 0
