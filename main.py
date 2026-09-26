#!/usr/bin/env python3
"""
Aplicación principal - Lector IA
Aplicación offline para leer en voz alta documentos e imágenes.
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.main_window import main

if __name__ == "__main__":
    main()
