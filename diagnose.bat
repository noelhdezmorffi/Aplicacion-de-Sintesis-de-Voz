@echo off
REM Script inteligente de diagnóstico de Python
REM Detecta problemas y sugiere soluciones

chcp 65001 >nul
color 0F
cls

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║          DIAGNÓSTICO DE PYTHON                    ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Test 1: Python en PATH
echo [1/3] Verificando si Python está en PATH...
where python >nul 2>&1
if errorlevel 1 (
    echo.
    echo ✗ Python NO está disponible en PATH
    echo.
    echo SOLUCIONES:
    echo.
    echo A) Python no está instalado:
    echo    - Descarga desde: https://www.python.org/downloads/
    echo    - Marca "Add Python to PATH"
    echo    - Reinicia tu computadora
    echo.
    echo B) Python está instalado pero no en PATH:
    echo    - Abre: Control Panel ^> Programs ^> Programs and Features
    echo    - Selecciona Python
    echo    - Haz clic en Modify
    echo    - Marca "Add Python to PATH"
    echo    - Reinicia tu computadora
    echo.
    echo C) Intenta con 'py':
    py --version >nul 2>&1
    if errorlevel 1 (
        echo    - El alias 'py' tampoco funciona
        echo    - Python probablemente no está instalado
    ) else (
        echo    - El alias 'py' SÍ funciona
        echo    - Puedes usar: py install.bat
        echo    - O crea un archivo: python.bat
        echo      Contenido: @echo off ^& py %%*
    )
    echo.
    pause
    exit /b 1
) else (
    echo ✓ Python está en PATH
)

REM Test 2: Versión de Python
echo.
echo [2/3] Verificando versión de Python...
python --version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo.
echo ✓ Versión: %PYVER%

REM Test 3: Verificar que funciona
echo.
echo [3/3] Verificando que Python funciona...
python -c "import sys; print('  ✓ Python funciona correctamente')" >nul 2>&1
if errorlevel 1 (
    echo ✗ Error al ejecutar Python
    pause
    exit /b 1
) else (
    python -c "import sys; print('  ✓ Ruta: ' + sys.executable)"
)

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  ✓ PYTHON ESTÁ CORRECTAMENTE INSTALADO            ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo Ahora puedes ejecutar: install.bat
echo.
pause
exit /b 0
