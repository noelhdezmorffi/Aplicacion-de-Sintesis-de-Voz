@echo off
REM Ejecutar la aplicación Lector IA
REM Versión para Windows

color 0A
title Lector IA - Aplicación de Lectura de Voz

echo.
echo ====================================
echo      LECTOR IA - INICIANDO...
echo ====================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo ERROR: Entorno virtual no encontrado
    echo Por favor ejecuta install.bat primero
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Ejecutar la aplicación
python main.py

if errorlevel 1 (
    echo.
    echo ERROR al ejecutar la aplicación
    echo Por favor verifica que todas las dependencias estén instaladas
    echo Ejecuta: pip install -r requirements.txt
    pause
)
