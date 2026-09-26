"""
Script de prueba - Verifica que todos los módulos funcionen correctamente
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Prueba que todos los módulos se importen correctamente."""
    print("=" * 50)
    print("Pruebas de Importación")
    print("=" * 50)
    print()
    
    try:
        print("[*] Importando módulos principales...")
        from modules.text_extractor import TextExtractor, ScreenReader
        print("  ✓ TextExtractor")
        print("  ✓ ScreenReader")
        
        from modules.text_to_speech import TextToSpeech
        print("  ✓ TextToSpeech")
        
        from ui.main_window import AITextReaderApp
        print("  ✓ AITextReaderApp")
        
        from utils.helpers import get_supported_formats
        print("  ✓ helpers")
        
        print("\n✓ Todos los módulos importados correctamente\n")
        return True
    
    except ImportError as e:
        print(f"\n✗ Error de importación: {e}\n")
        return False
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}\n")
        return False


def test_text_extractor():
    """Prueba el módulo de extracción de texto."""
    print("=" * 50)
    print("Pruebas del Extractor de Texto")
    print("=" * 50)
    print()
    
    try:
        from modules.text_extractor import TextExtractor
        
        extractor = TextExtractor()
        print("[*] Formatos soportados:")
        for fmt in sorted(extractor.supported_formats.keys()):
            print(f"  • {fmt}")
        
        print("\n✓ TextExtractor funcionando correctamente\n")
        return True
    
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        return False


def test_text_to_speech():
    """Prueba el módulo de síntesis de voz."""
    print("=" * 50)
    print("Pruebas de Síntesis de Voz")
    print("=" * 50)
    print()
    
    try:
        from modules.text_to_speech import TextToSpeech
        
        tts = TextToSpeech()
        print("[*] Voces disponibles:")
        
        voices = tts.get_voices()
        for i, voice in enumerate(voices):
            print(f"  {i}. {voice.name}")
        
        print(f"\n[*] Configuración actual:")
        print(f"  • Velocidad: 150 ppm")
        print(f"  • Volumen: 0.9")
        
        print("\n✓ TextToSpeech funcionando correctamente\n")
        return True
    
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        return False


def main():
    """Ejecuta todas las pruebas."""
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 10 + "SCRIPT DE PRUEBA - LECTOR IA" + " " * 10 + "║")
    print("╚" + "=" * 48 + "╝")
    print()
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Importación de módulos", test_imports()))
    results.append(("Extractor de texto", test_text_extractor()))
    results.append(("Síntesis de voz", test_text_to_speech()))
    
    # Resumen
    print("=" * 50)
    print("Resumen de Pruebas")
    print("=" * 50)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASÓ" if result else "✗ FALLÓ"
        print(f"  {status}: {test_name}")
    
    print()
    print(f"Resultado: {passed}/{total} pruebas pasadas")
    print()
    
    if passed == total:
        print("╔" + "=" * 48 + "╗")
        print("║" + " " * 15 + "✓ LISTO PARA USAR" + " " * 17 + "║")
        print("╚" + "=" * 48 + "╝")
        print()
        print("Para ejecutar la aplicación:")
        print("  • Windows: run.bat")
        print("  • Linux/Mac: ./run.sh")
        print()
        return 0
    
    else:
        print("╔" + "=" * 48 + "╗")
        print("║" + " " * 10 + "⚠️ HAY ERRORES QUE CORREGIR" + " " * 11 + "║")
        print("╚" + "=" * 48 + "╝")
        print()
        print("Verifica la documentación en README.md")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
