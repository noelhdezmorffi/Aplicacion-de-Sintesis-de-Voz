"""
Configuración global de la aplicación Lector IA
"""

import os
from pathlib import Path

# Directorio de la aplicación
APP_DIR = Path(__file__).parent.parent.parent
SRC_DIR = APP_DIR / "src"
MODULES_DIR = SRC_DIR / "modules"
UI_DIR = SRC_DIR / "ui"

# Configuración de síntesis de voz
VOICE_RATE_DEFAULT = 150  # palabras por minuto
VOICE_RATE_MIN = 50
VOICE_RATE_MAX = 300
VOICE_VOLUME_DEFAULT = 0.9  # 0.0 - 1.0

# Configuración de OCR
OCR_LANGUAGE_DEFAULT = "spa+eng"  # Español + Inglés
TESSERACT_PATH = os.environ.get(
    'TESSERACT_CMD',
    r'C:\Users\neutr\Desktop\proyectos\tesseract\tesseract.exe'
)

# Tamaño máximo de archivo (MB)
MAX_FILE_SIZE = 100

# Configuración de interfaz
UI_THEME = "default"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Idiomas soportados
SUPPORTED_LANGUAGES = ["spa", "eng", "fra", "deu"]

# Log
DEBUG_MODE = False
LOG_FILE = APP_DIR / "app.log"
