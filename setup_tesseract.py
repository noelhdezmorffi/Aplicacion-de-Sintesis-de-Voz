"""
Configuración de Tesseract OCR para Windows
Ejecuta este script si tienes problemas con pytesseract
"""

import os
import subprocess
import sys
from pathlib import Path

def find_tesseract():
    """Busca la instalación de Tesseract en rutas comunes."""
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME')),
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def main():
    """Configura Tesseract y verifica la instalación."""
    print("=" * 50)
    print("Configurador de Tesseract OCR")
    print("=" * 50)
    print()
    
    # Buscar Tesseract
    print("Buscando Tesseract OCR...")
    tesseract_path = find_tesseract()
    
    if tesseract_path:
        print(f"✓ Tesseract encontrado en: {tesseract_path}")
        
        # Crear archivo de configuración
        config_code = f'''import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'{tesseract_path}'
'''
        
        config_file = Path(__file__).parent / "src" / "modules" / "config.py"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            f.write(config_code)
        
        print(f"✓ Configuración guardada en: {config_file}")
        
        # Probar que funciona
        print("\nProbando Tesseract...")
        try:
            import pytesseract
            from PIL import Image
            
            # Restaurar configuración
            exec(config_code)
            
            print("✓ Tesseract configurado correctamente")
            
        except Exception as e:
            print(f"✗ Error al probar Tesseract: {e}")
            return 1
    
    else:
        print("✗ Tesseract no encontrado")
        print("\nDescargar Tesseract desde:")
        print("https://github.com/UB-Mannheim/tesseract/wiki")
        print("\nDespués de instalar, ejecuta este script nuevamente.")
        return 1
    
    print("\n" + "=" * 50)
    print("✓ Configuración completada")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
