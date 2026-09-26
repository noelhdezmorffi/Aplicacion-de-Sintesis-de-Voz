#!/bin/bash
# Script de instalación para Linux/Mac

echo "=========================================="
echo "Instalador - Lector IA"
echo "=========================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    exit 1
fi

echo "[✓] Python detectado"
echo ""

# Crear entorno virtual
echo "[*] Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "[*] Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Instalar Tesseract según el sistema
echo ""
echo "[*] Instalando Tesseract OCR..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Sistema: Linux"
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr espeak espeak-ng
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Sistema: macOS"
    if ! command -v brew &> /dev/null; then
        echo "Homebrew no está instalado. Por favor instálalo desde: https://brew.sh"
    else
        brew install tesseract
    fi
fi

echo ""
echo "[✓] Instalación completada!"
echo ""
echo "Para ejecutar la aplicación:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
