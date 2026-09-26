#!/bin/bash
# Ejecutar la aplicación Lector IA
# Versión para Linux/Mac

echo ""
echo "===================================="
echo "      LECTOR IA - INICIANDO..."
echo "===================================="
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "ERROR: Entorno virtual no encontrado"
    echo "Por favor ejecuta install.sh primero"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Ejecutar la aplicación
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR al ejecutar la aplicación"
    echo "Por favor verifica que todas las dependencias estén instaladas"
    echo "Ejecuta: pip install -r requirements.txt"
fi
