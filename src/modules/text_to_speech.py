"""
Módulo para síntesis de voz offline usando pyttsx3.
"""

import pyttsx3
import threading
import time
from typing import Optional, Callable
from enum import Enum


class VoiceEngine(Enum):
    """Motores de síntesis disponibles."""
    SAPI5 = "sapi5"  # Windows
    ESPEAK = "espeak"  # Linux/Mac


class TextToSpeech:
    """Convierte texto a voz con controles de reproducción.

    Implementa una pausa/resume aproximada calculando una estimación
    de la posición a partir del tiempo transcurrido y la velocidad
    configurada, ya que `pyttsx3` no provee control fino de posición.
    """

    def __init__(self):
        """Inicializa el motor de síntesis de voz."""
        self.engine = pyttsx3.init()
        self.is_speaking = False
        self.is_paused = False
        self.current_text = ""
        self.current_position = 0  # posición en caracteres dentro de current_text
        self.start_time: Optional[float] = None
        self.speech_thread: Optional[threading.Thread] = None

        # Configura parámetros por defecto
        self.engine.setProperty('rate', 180)  # Velocidad en palabras por minuto
        self.engine.setProperty('volume', 0.9)  # Volumen

        # Callbacks
        self.on_start: Optional[Callable] = None
        self.on_end: Optional[Callable] = None

    def set_rate(self, rate: int) -> None:
        """Establece la velocidad de lectura (50-300)."""
        rate = max(50, min(300, rate))
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float) -> None:
        """Establece el volumen (0.0-1.0)."""
        volume = max(0.0, min(1.0, volume))
        self.engine.setProperty('volume', volume)

    def get_voices(self) -> list:
        """Obtiene lista de voces disponibles."""
        return self.engine.getProperty('voices')

    def set_voice(self, voice_id: int = 0) -> None:
        """Establece la voz a usar."""
        voices = self.engine.getProperty('voices')
        if voice_id < len(voices):
            self.engine.setProperty('voice', voices[voice_id].id)

    def _start_speech(self, text_to_speak: str, start_offset: int = 0, use_thread: bool = True) -> None:
        """Inicia la reproducción del texto (subcadena) y registra tiempos."""
        # Mantener el texto completo y la posición inicial
        if start_offset == 0:
            self.current_text = text_to_speak
            self.current_position = 0
        else:
            # Cuando se reanuda, text_to_speak normalmente es una subcadena
            # pero current_text debe mantenerse como texto completo
            # start_offset indica la posición dentro de current_text
            self.current_position = start_offset

        self.is_paused = False
        self.is_speaking = True
        self.start_time = time.time()

        if use_thread:
            self.speech_thread = threading.Thread(
                target=self._speak_threaded,
                args=(text_to_speak,),
                daemon=True
            )
            self.speech_thread.start()
        else:
            self._speak_threaded(text_to_speak)

    def speak(self, text: str, use_thread: bool = True) -> None:
        """Habla el texto completo proporcionado."""
        # Guardar texto completo y comenzar desde 0
        self.current_text = text
        self.current_position = 0
        self._start_speech(text, 0, use_thread=use_thread)

    def _speak_threaded(self, text: str) -> None:
        """Habla el texto en un hilo separado."""
        try:
            if self.on_start:
                try:
                    self.on_start()
                except Exception:
                    pass

            self.engine.say(text)
            self.engine.runAndWait()

            # Al completar, marcar como no hablando y posición al final
            self.is_speaking = False
            self.start_time = None
            self.current_position = len(self.current_text)

            if self.on_end:
                try:
                    self.on_end()
                except Exception:
                    pass

        except Exception as e:
            print(f"Error al hablar: {e}")
            self.is_speaking = False
            self.start_time = None

    def speak_from_position(self, text: str, position: int, use_thread: bool = True) -> None:
        """Habla desde una posición específica del texto (posición en caracteres)."""
        # Guardar texto completo
        self.current_text = text
        # Tomar subcadena desde posición
        text_to_speak = text[position:]
        self._start_speech(text_to_speak, start_offset=position, use_thread=use_thread)

    def pause(self) -> None:
        """Pausa la reproducción (estimación de posición).

        Nota: `pyttsx3` no permite pausar nativamente; se detiene la reproducción
        y se estima la posición usando el tiempo transcurrido y la velocidad.
        """
        if self.is_speaking and not self.is_paused:
            # Calcular tiempo transcurrido desde que empezó la reproducción
            if self.start_time is not None:
                elapsed = time.time() - self.start_time
                rate_wpm = self.engine.getProperty('rate')  # palabras por minuto
                # Aproximación: una palabra ~6 caracteres (incluye espacios)
                chars_per_sec = (rate_wpm * 6) / 60.0
                spoken_chars = int(elapsed * chars_per_sec)
                self.current_position = min(len(self.current_text), self.current_position + spoken_chars)

            # Marcar pausado y detener motor sin resetear current_position
            self.is_paused = True
            self.is_speaking = False
            self.start_time = None
            try:
                self.engine.stop()
            except Exception:
                pass

    def resume(self) -> None:
        """Reanuda la reproducción desde la posición estimada."""
        if self.is_paused and self.current_text:
            self.is_paused = False
            # Reanudar desde la posición estimada
            pos = max(0, min(self.current_position, len(self.current_text)))
            self.speak_from_position(self.current_text, pos)

    def stop(self) -> None:
        """Detiene la reproducción y reinicia el estado."""
        try:
            self.engine.stop()
        except Exception:
            pass
        self.is_speaking = False
        self.is_paused = False
        self.start_time = None
        self.current_position = 0
        self.current_text = ""

    def get_available_languages(self) -> list:
        """Obtiene idiomas disponibles."""
        return ['spa', 'eng', 'fra', 'deu']

    def __del__(self):
        """Limpia recursos al destruir."""
        try:
            self.stop()
        except Exception:
            pass

    def export_to_file(self, text: str, file_path: str) -> bool:
        """Exporta el texto proporcionado a un archivo de audio.

        Args:
            text: Texto a sintetizar.
            file_path: Ruta del archivo de salida (ej. .wav).

        Returns:
            True si la exportación fue exitosa, False en caso contrario.
        """
        try:
            # Guardar estado temporalmente
            # Usamos save_to_file y runAndWait para generar el archivo
            self.engine.save_to_file(text, file_path)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error al exportar audio: {e}")
            return False
