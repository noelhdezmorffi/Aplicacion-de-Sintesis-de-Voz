"""
Ejemplo de uso de los módulos de Lector IA
Muestra cómo usar la aplicación desde código Python
"""

import sys
import os
import time

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.text_extractor import TextExtractor, ScreenReader
from modules.text_to_speech import TextToSpeech


def example_1_extract_pdf():
    """Ejemplo 1: Extraer texto de un PDF y leerlo."""
    print("\n" + "=" * 60)
    print("Ejemplo 1: Extraer y Leer un PDF")
    print("=" * 60)
    
    # Crear instancia del extractor
    extractor = TextExtractor()
    
    # Extraer texto (cambiar ruta a un PDF válido)
    pdf_path = "documentos/ejemplo.pdf"  # Cambiar a una ruta válida
    
    if os.path.exists(pdf_path):
        print(f"\n[*] Extrayendo texto de: {pdf_path}")
        text = extractor.extract_text(pdf_path)
        
        if text:
            print(f"[✓] Texto extraído ({len(text)} caracteres)")
            print(f"\nPrimeros 200 caracteres:\n{text[:200]}...\n")
            
            # Leer el texto
            print("[*] Iniciando síntesis de voz...")
            tts = TextToSpeech()
            tts.set_rate(150)  # Velocidad normal
            tts.speak(text[:500])  # Leer primeros 500 caracteres
            
            print("[✓] Lectura completada")
        else:
            print("✗ No se pudo extraer texto")
    else:
        print(f"✗ Archivo no encontrado: {pdf_path}")


def example_2_extract_image():
    """Ejemplo 2: Extraer texto de una imagen."""
    print("\n" + "=" * 60)
    print("Ejemplo 2: Extraer Texto de una Imagen (OCR)")
    print("=" * 60)
    
    extractor = TextExtractor()
    
    # Imagen de ejemplo (cambiar a una imagen válida)
    image_path = "documentos/ejemplo.jpg"  # Cambiar a una ruta válida
    
    if os.path.exists(image_path):
        print(f"\n[*] Extrayendo texto de imagen: {image_path}")
        print("[*] Esto puede tardar unos segundos...")
        
        text = extractor.extract_text(image_path)
        
        if text:
            print(f"[✓] Texto extraído ({len(text)} caracteres)")
            print(f"\nTexto detectado:\n{text[:500]}...\n")
        else:
            print("✗ No se pudo extraer texto de la imagen")
    else:
        print(f"✗ Archivo no encontrado: {image_path}")


def example_3_text_to_speech():
    """Ejemplo 3: Síntesis de voz básica."""
    print("\n" + "=" * 60)
    print("Ejemplo 3: Síntesis de Voz Básica")
    print("=" * 60)
    
    tts = TextToSpeech()
    
    # Mostrar voces disponibles
    print("\n[*] Voces disponibles:")
    voices = tts.get_voices()
    for i, voice in enumerate(voices):
        print(f"  {i}. {voice.name}")
    
    # Texto a leer
    texto = "Hola, este es un ejemplo de síntesis de voz. La aplicación Lector IA puede leer documentos, imágenes y el contenido de tu pantalla."
    
    print(f"\n[*] Leyendo: {texto}")
    print("[*] Escucha el audio...")
    
    tts.speak(texto)
    print("[✓] Lectura completada")


def example_4_screen_reader():
    """Ejemplo 4: Lector de pantalla (OCR)."""
    print("\n" + "=" * 60)
    print("Ejemplo 4: Lector de Pantalla (OCR)")
    print("=" * 60)
    
    screen_reader = ScreenReader()
    
    print("\n[*] Capturando contenido de la pantalla...")
    print("[*] Esto puede tardar unos segundos...")
    
    text = screen_reader.capture_screen_text()
    
    if text:
        print(f"[✓] Texto capturado ({len(text)} caracteres)")
        print(f"\nPrimeros 300 caracteres:\n{text[:300]}...\n")
    else:
        print("✗ No se pudo capturar texto de la pantalla")


def example_5_word_document():
    """Ejemplo 5: Extraer texto de un documento Word."""
    print("\n" + "=" * 60)
    print("Ejemplo 5: Extraer Texto de un Documento Word")
    print("=" * 60)
    
    extractor = TextExtractor()
    
    # Documento Word (cambiar a una ruta válida)
    doc_path = "documentos/ejemplo.docx"  # Cambiar a una ruta válida
    
    if os.path.exists(doc_path):
        print(f"\n[*] Extrayendo texto de: {doc_path}")
        text = extractor.extract_text(doc_path)
        
        if text:
            print(f"[✓] Texto extraído ({len(text)} caracteres)")
            print(f"\nPrimeros 300 caracteres:\n{text[:300]}...\n")
        else:
            print("✗ No se pudo extraer texto")
    else:
        print(f"✗ Archivo no encontrado: {doc_path}")


def example_6_control_voice():
    """Ejemplo 6: Control de parámetros de voz."""
    print("\n" + "=" * 60)
    print("Ejemplo 6: Control de Parámetros de Voz")
    print("=" * 60)
    
    tts = TextToSpeech()
    texto = "Este es un ejemplo con controles de velocidad y volumen."
    
    # Velocidad lenta
    print("\n[*] Lectura LENTA (100 ppm)...")
    tts.set_rate(100)
    tts.speak(texto)
    
    time.sleep(2)
    
    # Velocidad normal
    print("[*] Lectura NORMAL (150 ppm)...")
    tts.set_rate(150)
    tts.speak(texto)
    
    time.sleep(2)
    
    # Velocidad rápida
    print("[*] Lectura RÁPIDA (200 ppm)...")
    tts.set_rate(200)
    tts.speak(texto)
    
    print("[✓] Ejemplo completado")


def main():
    """Ejecuta los ejemplos."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "EJEMPLOS DE USO - LECTOR IA" + " " * 19 + "║")
    print("╚" + "=" * 58 + "╝")
    
    ejemplos = [
        ("Síntesis de voz básica", example_3_text_to_speech),
        ("Control de parámetros de voz", example_6_control_voice),
    ]
    
    print("\nEjemplos que se pueden ejecutar:")
    for i, (nombre, _) in enumerate(ejemplos, 1):
        print(f"  {i}. {nombre}")
    
    print("\nNota: Los siguientes ejemplos requieren archivos específicos:")
    print("  - Extraer PDF")
    print("  - Extraer Imagen")
    print("  - Lector de Pantalla")
    print("  - Documento Word")
    
    print("\n" + "=" * 60)
    
    # Ejecutar ejemplos disponibles
    try:
        example_3_text_to_speech()
    except KeyboardInterrupt:
        print("\n[*] Ejemplo detenido por el usuario")
    except Exception as e:
        print(f"\n✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("\nPara usar la aplicación gráfica:")
    print("  • Windows: run.bat")
    print("  • Linux/Mac: ./run.sh")
    print()


if __name__ == "__main__":
    main()
