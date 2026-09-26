"""
API de Referencia - Lector IA
Ejemplos avanzados de uso de los módulos
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.text_extractor import TextExtractor, ScreenReader
from modules.text_to_speech import TextToSpeech


# ==============================================================================
# EJEMPLO 1: USO BÁSICO DE TextExtractor
# ==============================================================================

def ejemplo_text_extractor_basico():
    """Ejemplo básico de extracción de texto."""
    extractor = TextExtractor()
    
    # Ver formatos soportados
    print("Formatos soportados:")
    for fmt in extractor.supported_formats.keys():
        print(f"  • {fmt}")
    
    # Extraer texto de un archivo
    archivo = "documento.pdf"
    texto = extractor.extract_text(archivo)
    
    if texto:
        print(f"Texto extraído: {len(texto)} caracteres")
    else:
        print("Error al extraer texto")


# ==============================================================================
# EJEMPLO 2: PROCESAMIENTO DE ARCHIVOS CON VALIDACIÓN
# ==============================================================================

def ejemplo_procesamiento_con_validacion():
    """Procesa archivos con validación de tamaño."""
    extractor = TextExtractor()
    
    archivos = ["doc1.pdf", "doc2.jpg", "doc3.docx"]
    
    for archivo in archivos:
        try:
            # Verificar existencia
            if not os.path.exists(archivo):
                print(f"[!] No existe: {archivo}")
                continue
            
            # Verificar tamaño
            tamaño_mb = os.path.getsize(archivo) / (1024 * 1024)
            if tamaño_mb > 100:
                print(f"[!] Archivo muy grande: {archivo} ({tamaño_mb:.2f} MB)")
                continue
            
            # Extraer
            print(f"[*] Procesando: {archivo}")
            texto = extractor.extract_text(archivo)
            print(f"[✓] Extraído: {len(texto)} caracteres")
            
        except Exception as e:
            print(f"[✗] Error: {e}")


# ==============================================================================
# EJEMPLO 3: USO AVANZADO DE TextToSpeech
# ==============================================================================

def ejemplo_text_to_speech_avanzado():
    """Ejemplos avanzados de síntesis de voz."""
    tts = TextToSpeech()
    
    # 1. Listar voces disponibles
    print("Voces disponibles:")
    voices = tts.get_voices()
    for i, voice in enumerate(voices):
        print(f"  {i}. {voice.name}")
    
    # 2. Cambiar configuración
    tts.set_rate(200)  # Rápido
    tts.set_volume(0.8)  # Volumen 80%
    tts.set_voice(0)  # Primera voz
    
    # 3. Hablar
    texto = "Ejemplo de síntesis de voz avanzada"
    tts.speak(texto)


# ==============================================================================
# EJEMPLO 4: LECTURA DE PANTALLA
# ==============================================================================

def ejemplo_screen_reader():
    """Captura y lee texto de la pantalla."""
    screen_reader = ScreenReader()
    
    print("Capturando pantalla...")
    texto = screen_reader.capture_screen_text()
    
    if texto:
        print(f"Texto capturado: {len(texto)} caracteres")
        print(f"Vista previa:\n{texto[:200]}...")
        
        # Leer el texto capturado
        tts = TextToSpeech()
        tts.speak(texto[:500])
    else:
        print("No se pudo capturar texto")


# ==============================================================================
# EJEMPLO 5: PROCESAMIENTO EN LOTE
# ==============================================================================

def ejemplo_procesamiento_lote():
    """Procesa múltiples archivos en lote."""
    extractor = TextExtractor()
    
    archivos = [
        "documento1.pdf",
        "documento2.docx",
        "imagen1.jpg",
    ]
    
    resultados = {}
    
    for archivo in archivos:
        print(f"Procesando: {archivo}...")
        texto = extractor.extract_text(archivo)
        
        if texto:
            resultados[archivo] = {
                'exito': True,
                'caracteres': len(texto),
                'palabras': len(texto.split()),
                'texto_preview': texto[:100],
            }
        else:
            resultados[archivo] = {
                'exito': False,
                'error': 'No se pudo extraer',
            }
    
    # Mostrar resultados
    print("\nResultados:")
    for archivo, resultado in resultados.items():
        if resultado['exito']:
            print(f"  ✓ {archivo}: {resultado['caracteres']} chars, {resultado['palabras']} palabras")
        else:
            print(f"  ✗ {archivo}: {resultado['error']}")


# ==============================================================================
# EJEMPLO 6: COMBINACIÓN DE MÓDULOS
# ==============================================================================

def ejemplo_flujo_completo():
    """Flujo completo: extraer → procesar → leer."""
    
    extractor = TextExtractor()
    tts = TextToSpeech()
    
    # 1. Extraer
    archivo = "documento.pdf"
    print(f"1. Extrayendo de: {archivo}")
    texto = extractor.extract_text(archivo)
    
    if not texto:
        print("Error al extraer")
        return
    
    print(f"   ✓ Extraído: {len(texto)} caracteres")
    
    # 2. Procesar
    print(f"2. Procesando texto...")
    
    # Limitar a primeros 2000 caracteres
    texto_procesado = texto[:2000]
    num_palabras = len(texto_procesado.split())
    print(f"   ✓ Procesado: {num_palabras} palabras")
    
    # 3. Configurar voz
    print(f"3. Configurando voz...")
    tts.set_rate(150)  # Velocidad normal
    tts.set_volume(0.9)  # Volumen alto
    print(f"   ✓ Configurado")
    
    # 4. Leer
    print(f"4. Leyendo...")
    tts.speak(texto_procesado)
    print(f"   ✓ Lectura completada")


# ==============================================================================
# EJEMPLO 7: MANEJO DE ERRORES
# ==============================================================================

def ejemplo_manejo_errores():
    """Manejo robusto de errores."""
    extractor = TextExtractor()
    
    # Caso 1: Archivo no existe
    try:
        texto = extractor.extract_text("archivo_inexistente.pdf")
        if texto is None:
            print("Archivo no existe")
    except FileNotFoundError as e:
        print(f"Error de archivo: {e}")
    
    # Caso 2: Formato no soportado
    try:
        texto = extractor.extract_text("archivo.xyz")
        if texto is None:
            print("Formato no soportado")
    except ValueError as e:
        print(f"Error de formato: {e}")
    
    # Caso 3: Error general
    try:
        archivo = None
        extractor.extract_text(archivo)
    except Exception as e:
        print(f"Error inesperado: {e}")


# ==============================================================================
# EJEMPLO 8: USO CON THREADING (Para aplicaciones)
# ==============================================================================

def ejemplo_threading():
    """Ejemplo de uso con threading (no bloquea la interfaz)."""
    import threading
    import time
    
    def leer_archivo_en_hilo():
        extractor = TextExtractor()
        tts = TextToSpeech()
        
        # Extraer
        texto = extractor.extract_text("documento.pdf")
        
        # Leer en hilo separado
        def speak_threaded():
            tts.speak(texto, use_thread=False)
        
        thread = threading.Thread(target=speak_threaded, daemon=True)
        thread.start()
        
        # La interfaz principal no se congela
        print("Interfaz respondiendo mientras se lee...")
    
    leer_archivo_en_hilo()


# ==============================================================================
# MAIN - EJECUTAR EJEMPLOS
# ==============================================================================

def main():
    """Menú de ejemplos."""
    ejemplos = [
        ("1", "TextExtractor básico", ejemplo_text_extractor_basico),
        ("2", "Procesamiento con validación", ejemplo_procesamiento_con_validacion),
        ("3", "TextToSpeech avanzado", ejemplo_text_to_speech_avanzado),
        ("4", "Screen Reader", ejemplo_screen_reader),
        ("5", "Procesamiento en lote", ejemplo_procesamiento_lote),
        ("6", "Flujo completo", ejemplo_flujo_completo),
        ("7", "Manejo de errores", ejemplo_manejo_errores),
    ]
    
    print("=" * 60)
    print("EJEMPLOS AVANZADOS - LECTOR IA")
    print("=" * 60)
    print("\nEjemplos disponibles:")
    
    for id, nombre, _ in ejemplos:
        print(f"  {id}. {nombre}")
    
    print("\nNota: Estos son ejemplos de referencia.")
    print("Para usar la interfaz gráfica, ejecuta: python main.py")
    print()


if __name__ == "__main__":
    main()
