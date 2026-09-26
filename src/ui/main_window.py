"""
Interfaz gráfica principal de la aplicación.
"""

import sys
import os
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QLabel, QComboBox, QSpinBox, QDoubleSpinBox,
    QTextEdit, QFileDialog, QMessageBox, QProgressBar, QTabWidget
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QIcon
import logging

# configure a simple logger for debugging export/ui issues
logging.basicConfig(
    filename='export_debug.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)

# Importar módulos propios
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
from modules.text_extractor import TextExtractor
from modules.text_to_speech import TextToSpeech


class SpeechWorker(QThread):
    """Worker para ejecutar síntesis de voz en hilo separado."""
    
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, text_to_speech: TextToSpeech, text: str, position: int = 0):
        super().__init__()
        self.tts = text_to_speech
        self.text = text
        self.position = position
    
    def run(self):
        """Ejecuta la síntesis de voz."""
        try:
            if self.position > 0:
                # Ejecutar de forma bloqueante dentro del QThread
                self.tts.speak_from_position(self.text, self.position, use_thread=False)
            else:
                self.tts.speak(self.text, use_thread=False)
            # Emitir finished cuando termine la reproducción bloqueante
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class SampleWorker(QThread):
    """Worker para reproducir una muestra de voz sin bloquear la UI."""

    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, text: str, rate: int, volume: float, voice_index: int):
        super().__init__()
        self.text = text
        self.rate = rate
        self.volume = volume
        self.voice_index = voice_index

    def run(self):
        try:
            # Crear una instancia separada de TTS en este thread para evitar conflictos
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)
            
            # Establecer voz
            voices = engine.getProperty('voices')
            if self.voice_index < len(voices):
                engine.setProperty('voice', voices[self.voice_index].id)
            
            # Reproducir
            engine.say(self.text)
            engine.runAndWait()
            
            # Limpiar
            try:
                engine.stop()
            except Exception:
                pass
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class ExportWorker(QThread):
    """Worker para exportar audio a archivo sin bloquear la UI.

    Crea una instancia propia de pyttsx3 en el hilo para evitar conflictos
    con el motor compartido en la aplicación principal.
    """

    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text: str, file_path: str, rate: int = 150, volume: float = 0.9, voice_index: int = 0):
        super().__init__()
        self.text = text
        self.file_path = file_path
        self.rate = rate
        self.volume = volume
        self.voice_index = voice_index

    def run(self):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            try:
                engine.setProperty('rate', self.rate)
                engine.setProperty('volume', self.volume)
                voices = engine.getProperty('voices')
                if 0 <= self.voice_index < len(voices):
                    engine.setProperty('voice', voices[self.voice_index].id)
            except Exception:
                pass

            # Guardar a archivo
            engine.save_to_file(self.text, self.file_path)
            engine.runAndWait()
            try:
                engine.stop()
            except Exception:
                pass

            logging.getLogger('lector_ia').info(f"ExportWorker: finished writing {self.file_path}")
            self.finished.emit(self.file_path)
        except Exception as e:
            logging.getLogger('lector_ia').exception(f"ExportWorker error: {e}")
            self.error.emit(str(e))


class AITextReaderApp(QMainWindow):
    """Aplicación principal de lectura de texto con IA."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lector IA - Lee en Voz Alta")
        # Iniciar en ventana pequeña (todos los botones visibles)
        self.resize(900, 600)
        self.setMinimumSize(600, 400)
        
        # Inicializar módulos
        self.text_extractor = TextExtractor()
        self.tts = TextToSpeech()
        
        # Variables de estado
        self.current_text = ""
        self.current_file = None
        self.speech_worker: Optional[SpeechWorker] = None
        self.is_paused = False
        self.pause_position = 0
        
        # Crear interfaz
        self.init_ui()
        
        # Timer para actualizar estado
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(500)
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Crear tabs
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Tab 1: Archivo
        file_tab = QWidget()
        tabs.addTab(file_tab, "📄 Leer Archivo")
        self.setup_file_tab(file_tab)
        
        # Tab 2: Configuración
        config_tab = QWidget()
        tabs.addTab(config_tab, "⚙️ Configuración")
        self.setup_config_tab(config_tab)
        
        # Barra de estado inferior
        self.setup_status_bar()
    
    def setup_file_tab(self, parent: QWidget):
        """Configura la pestaña de lectura de archivos."""
        layout = QVBoxLayout()
        
        # Botones de archivo
        button_layout = QHBoxLayout()
        
        self.open_file_btn = QPushButton("📂 Abrir Archivo")
        self.open_file_btn.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_file_btn)
        
        self.clear_btn = QPushButton("🗑️ Limpiar")
        self.clear_btn.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_btn)
        
        layout.addLayout(button_layout)
        
        # Área de texto
        layout.addWidget(QLabel("📝 Texto extraído:"))
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Courier", 10))
        layout.addWidget(self.text_edit)
        
        # Controles de reproducción
        self.setup_playback_controls(layout)
        
        parent.setLayout(layout)
    
    def setup_config_tab(self, parent: QWidget):
        """Configura la pestaña de configuración."""
        layout = QVBoxLayout()
        
        # Velocidad de lectura
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("⏱️ Velocidad de lectura:"))
        self.speed_spinbox = QSpinBox()
        self.speed_spinbox.setMinimum(50)
        self.speed_spinbox.setMaximum(300)
        self.speed_spinbox.setValue(180)
        self.speed_spinbox.setSuffix(" ppm")
        self.speed_spinbox.valueChanged.connect(self.on_speed_changed)
        speed_layout.addWidget(self.speed_spinbox)
        layout.addLayout(speed_layout)
        
        # Volumen
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("🔊 Volumen:"))
        self.volume_spinbox = QDoubleSpinBox()
        self.volume_spinbox.setMinimum(0.0)
        self.volume_spinbox.setMaximum(1.0)
        self.volume_spinbox.setValue(0.9)
        self.volume_spinbox.setSingleStep(0.1)
        self.volume_spinbox.valueChanged.connect(self.on_volume_changed)
        volume_layout.addWidget(self.volume_spinbox)
        layout.addLayout(volume_layout)
        
        # Selección de voz
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("🎤 Voz:"))
        self.voice_combo = QComboBox()
        self.update_voice_list()
        self.voice_combo.currentIndexChanged.connect(self.on_voice_changed)
        voice_layout.addWidget(self.voice_combo)
        layout.addLayout(voice_layout)

        # Presets de voz (ajustan velocidad/volumen para distintos timbres)
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("🎚️ Preset de voz:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("Conversacional (por defecto)")
        self.preset_combo.addItem("Narrador (bajo, claro)")
        self.preset_combo.addItem("Anuncio (claro, enérgico)")
        self.preset_combo.addItem("Suave (calmado)")
        self.preset_combo.addItem("Rápido (dinámico)")
        self.preset_combo.currentIndexChanged.connect(self.apply_voice_preset)
        preset_layout.addWidget(self.preset_combo)
        layout.addLayout(preset_layout)

        # Botón para probar la voz actual
            # Botón 'Probar voz' eliminado (problemas intermitentes en cargas múltiples)

        # Botón para refrescar la lista de voces
        refresh_layout = QHBoxLayout()
        self.refresh_voices_btn = QPushButton("🔄 Refrescar voces")
        self.refresh_voices_btn.clicked.connect(self.refresh_voice_list)
        refresh_layout.addWidget(self.refresh_voices_btn)
        layout.addLayout(refresh_layout)
        
         # Información de voces disponibles
        voices_info = QLabel()
        voices = self.tts.get_voices()
        voice_text = "Voces disponibles en el sistema:\n\n"
        for i, voice in enumerate(voices):
            voice_text += f"{i}. {voice.name}\n"
        voices_info.setText(voice_text)
        layout.addWidget(voices_info)
        
        layout.addStretch()
        parent.setLayout(layout)
    
    def setup_playback_controls(self, layout: QVBoxLayout):
        """Configura los controles de reproducción."""
        # Layout de controles
        controls_layout = QHBoxLayout()
        
        # Botones
        # No se muestra botón de reproducción en la UI por petición del usuario
        
        layout.addLayout(controls_layout)
        
        # Barra de progreso
        # Barra de progreso eliminada por petición del usuario

        # Controles de exportar / abrir con reproductor externo
        external_layout = QHBoxLayout()
        self.save_btn = QPushButton("💾 Guardar audio")
        self.save_btn.clicked.connect(self.export_audio)
        self.save_btn.setEnabled(False)
        external_layout.addWidget(self.save_btn)

        # 'Abrir en reproductor' button removed per user request.

        layout.addLayout(external_layout)
    
    def setup_status_bar(self):
        """Configura la barra de estado."""
        self.status_label = QLabel("Listo")
        self.statusBar().addWidget(self.status_label)
    
    def open_file(self):
        """Abre un diálogo para seleccionar archivo."""
        # Detener audio si está reproduciéndose
        if self.is_paused or self.tts.is_speaking:
            self.tts.stop()
        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Abrir archivo",
            "",
            "Todos los archivos (*);;PDF (*.pdf);;Documentos (*.doc *.docx);;Imágenes (*.jpg *.jpeg *.png);;Texto (*.txt)"
        )
        
        if file_path:
            self.status_label.setText(f"Extrayendo texto de {Path(file_path).name}...")
            
            # Extraer texto
            text = self.text_extractor.extract_text(file_path)
            
            if text:
                self.current_text = text
                self.is_paused = False
                self.pause_position = 0
                
                # No hay botones de reproducción o barra de progreso
                
                self.text_edit.setText(text)
                self.status_label.setText(f"✓ {Path(file_path).name} cargado ({len(text)} caracteres)")
                # Habilitar botón de guardar/exportar audio cuando hay texto
                self.save_btn.setEnabled(True)

                # Registro y forzado de repintado: si el UI queda 'pegado' al cargar
                logging.getLogger('lector_ia').info(f"open_file: loaded {file_path}, enabling save_btn")
                try:
                    self.save_btn.repaint()
                    self.update()
                    QApplication.processEvents()
                except Exception:
                    logging.getLogger('lector_ia').exception('Error forcing repaint after open_file')

                # Deferred refresh as a robustness measure for repeated loads
                def _deferred_after_open():
                    logging.getLogger('lector_ia').info('Deferred UI refresh after open_file running')
                    try:
                        self.save_btn.setEnabled(True if self.current_text else False)
                        self.save_btn.repaint()
                        self.update()
                        QApplication.processEvents()
                    except Exception:
                        logging.getLogger('lector_ia').exception('Error in deferred refresh after open_file')

                QTimer.singleShot(500, _deferred_after_open)
            else:
                QMessageBox.warning(self, "Error", "No se pudo extraer texto del archivo.")
                self.status_label.setText("Error al extraer texto")
    
    def clear_text(self):
        """Limpia el área de texto."""
        # Detener audio si está reproduciéndose
        if self.is_paused or self.tts.is_speaking:
            self.tts.stop()
        
        self.text_edit.clear()
        self.current_text = ""
        self.current_file = None
        self.is_paused = False
        self.pause_position = 0
        
        # No hay botones de reproducción o barra de progreso
        
        self.status_label.setText("Texto limpiado")
        # Deshabilitar botones de export
        try:
            self.save_btn.setEnabled(False)
            if hasattr(self, 'exported_audio_path'):
                del self.exported_audio_path
        except Exception:
            pass
    
    def play_audio(self):
        """Inicia la reproducción de audio."""
        text = self.text_edit.toPlainText()
        
        if not text:
            QMessageBox.warning(self, "Advertencia", "No hay texto para leer.")
            return
        
        self.current_text = text
        self.is_paused = False
        self.pause_position = 0
        
        # Crear worker
        self.speech_worker = SpeechWorker(self.tts, text, 0)
        self.speech_worker.finished.connect(self.on_speech_finished)
        self.speech_worker.error.connect(self.on_speech_error)
        self.speech_worker.start()
        
        # Iniciado por programación; la UI no muestra controles de reproducción
        self.status_label.setText("▶️ Leyendo...")
        # Ensure export buttons are updated
        try:
            self.save_btn.setEnabled(True if text else False)
        except Exception:
            pass
    
    def pause_audio(self):
        """Pausa la reproducción."""
        # Mantener compatibilidad: pausar el motor TTS y actualizar estado
        if self.tts.is_speaking:
            try:
                self.tts.pause()
            except Exception:
                # si pause no está soportado, intentar detener y conservar posición estimada
                try:
                    self.tts.stop()
                except Exception:
                    pass
            try:
                self.pause_position = int(getattr(self.tts, 'current_position', len(self.current_text)//2))
            except Exception:
                self.pause_position = max(0, len(self.current_text) // 2)
            self.is_paused = True
            self.status_label.setText("⏸️ Pausado")
    
    def resume_audio(self):
        """Reanuda la reproducción."""
        if self.is_paused and self.current_text:
            self.is_paused = False
            pos = int(self.pause_position) if self.pause_position else 0
            # Crear worker para reanudar desde la posición guardada
            self.speech_worker = SpeechWorker(self.tts, self.current_text, pos)
            self.speech_worker.finished.connect(self.on_speech_finished)
            self.speech_worker.error.connect(self.on_speech_error)
            self.speech_worker.start()
            self.status_label.setText("▶️ Reanudando...")
        # Enable save button while playing
        try:
            self.save_btn.setEnabled(True if self.current_text else False)
        except Exception:
            pass
    
    def stop_audio(self):
        """Detiene la reproducción."""
        self.is_paused = False
        self.pause_position = 0
        self.tts.stop()
        self.status_label.setText("⏹️ Detenido")
        # Keep exported audio buttons available only if there's an exported file
        try:
            self.save_btn.setEnabled(True if self.current_text else False)
        except Exception:
            pass
    
    def on_speech_finished(self):
        """Se ejecuta cuando la síntesis de voz termina."""
        self.status_label.setText("✓ Lectura completada")
        # Update export/open buttons
        try:
            self.save_btn.setEnabled(True if self.current_text else False)
        except Exception:
            pass
    
    def on_speech_error(self, error: str):
        """Se ejecuta cuando hay error en síntesis de voz."""
        QMessageBox.critical(self, "Error", f"Error al leer: {error}")
        self.status_label.setText("Error en síntesis de voz")
        self.stop_audio()

    def export_audio(self):
        """Exporta el texto actual a un archivo de audio (.wav)."""
        text = self.text_edit.toPlainText()
        if not text:
            QMessageBox.warning(self, "Advertencia", "No hay texto para exportar.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar audio", "", "WAV Files (*.wav);;All Files (*)")
        if not file_path:
            return

        # Añadir extensión .wav si no la tiene
        if not Path(file_path).suffix:
            file_path = str(Path(file_path).with_suffix('.wav'))

        self.status_label.setText("Exportando audio...")
        self.save_btn.setEnabled(False)
        # Pasar parámetros de configuración actuales al worker para evitar usar el motor compartido
        rate = self.speed_spinbox.value()
        volume = self.volume_spinbox.value()
        voice_index = self.voice_combo.currentIndex()
        self.export_worker = ExportWorker(text, file_path, rate=rate, volume=volume, voice_index=voice_index)
        self.export_worker.finished.connect(self.on_export_finished)
        self.export_worker.error.connect(self.on_export_error)
        self.export_worker.start()

    def on_export_finished(self, file_path: str):
        """Callback cuando la exportación finaliza."""
        try:
            self.exported_audio_path = file_path
            file_name = Path(file_path).name

            logging.getLogger('lector_ia').info(f"on_export_finished called for {file_path}")
            self.status_label.setText(f"✓ Audio guardado: {file_name}")

            # Habilitar botones inmediatamente
            self.save_btn.setEnabled(True if self.current_text else False)

            # Procesar eventos para asegurar actualización visual
            QApplication.processEvents()

            # Forzar repintado del botón de guardar
            try:
                self.save_btn.repaint()
                self.update()
                QApplication.processEvents()
            except Exception:
                logging.getLogger('lector_ia').exception('Error forcing repaint in on_export_finished')

            # Deferred refresh to robustly ensure the UI updates after export
            def _deferred_refresh():
                logging.getLogger('lector_ia').info('Deferred UI refresh running (export finished)')
                try:
                    self.save_btn.setEnabled(True)
                    self.save_btn.repaint()
                    self.update()
                    QApplication.processEvents()
                except Exception:
                    logging.getLogger('lector_ia').exception('Error during deferred UI refresh')

            QTimer.singleShot(500, _deferred_refresh)

        except Exception as e:
            logging.getLogger('lector_ia').exception(f"Error en on_export_finished: {e}")
            self.save_btn.setEnabled(True if self.current_text else False)

    def on_export_error(self, error: str):
        """Maneja errores en exportación de audio."""
        try:
            QMessageBox.critical(self, "Error", f"Error exportando audio: {error}")
            self.status_label.setText("Error exportando audio")
        finally:
            # Asegurar que los botones se habiliten aunque haya error
            self.save_btn.setEnabled(True if self.current_text else False)

    def open_external_audio(self):
        """Abre el archivo de audio exportado con el reproductor por defecto del sistema."""
        # Function kept for potential future use but audio-open button was removed.
        path = getattr(self, 'exported_audio_path', None)
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Advertencia", "No hay archivo de audio exportado. Exporte primero.")
            return

        try:
            os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo: {e}")
    
    def on_speed_changed(self, value: int):
        """Actualiza la velocidad de lectura."""
        self.tts.set_rate(value)
    
    def on_volume_changed(self, value: float):
        """Actualiza el volumen."""
        self.tts.set_volume(value)
    
    def on_voice_changed(self, index: int):
        """Cambia la voz seleccionada."""
        self.tts.set_voice(index)

    def apply_voice_preset(self, index: int):
        """Aplica un preset de voz ajustando velocidad y volumen."""
        # Presets: (rate, volume)
        presets = {
            0: (150, 0.9),   # Conversacional
            1: (120, 1.0),   # Narrador
            2: (180, 1.0),   # Anuncio
            3: (120, 0.7),   # Suave
            4: (220, 1.0),   # Rápido
        }
        rate, vol = presets.get(index, (150, 0.9))
        # Actualizar controles sin disparar eventos recursivos innecesarios
        self.speed_spinbox.blockSignals(True)
        self.volume_spinbox.blockSignals(True)
        self.speed_spinbox.setValue(rate)
        self.volume_spinbox.setValue(vol)
        self.speed_spinbox.blockSignals(False)
        self.volume_spinbox.blockSignals(False)
        # Aplicar al motor TTS inmediatamente
        self.tts.set_rate(rate)
        self.tts.set_volume(vol)

    def test_voice_sample(self):
        """Reproduce una muestra corta de la voz seleccionada."""
        # Evitar crear múltiples workers si uno ya está en ejecución
        if hasattr(self, 'sample_worker') and self.sample_worker and self.sample_worker.isRunning():
            QMessageBox.warning(self, "Información", "Muestra en reproducción. Espera a que termine.")
            return
        
        sample_text = "Este es un ejemplo de voz. Comprueba la entonación, claridad y volumen."
        
        # Obtener configuración actual
        rate = self.speed_spinbox.value()
        volume = self.volume_spinbox.value()
        voice_index = self.voice_combo.currentIndex()

        # Ejecutar en worker con instancia de pyttsx3 separada
        self.test_voice_btn.setEnabled(False)
        self.sample_worker = SampleWorker(sample_text, rate, volume, voice_index)
        self.sample_worker.finished.connect(self.on_sample_finished)
        self.sample_worker.error.connect(self.on_sample_error)
        self.sample_worker.start()

    def on_sample_finished(self):
        """Callback cuando la muestra termina."""
        try:
            if hasattr(self, 'test_voice_btn'):
                try:
                    self.test_voice_btn.setEnabled(True)
                except Exception:
                    pass
            self.status_label.setText("Muestra reproducida")
        except Exception as e:
            print(f"Error en on_sample_finished: {e}")

    def on_sample_error(self, error: str):
        """Maneja errores en reproducción de muestra."""
        try:
            if hasattr(self, 'test_voice_btn'):
                try:
                    self.test_voice_btn.setEnabled(True)
                except Exception:
                    pass
            QMessageBox.critical(self, "Error", f"Error al reproducir muestra: {error}")
        except Exception as e:
            print(f"Error en on_sample_error: {e}")

    def refresh_voice_list(self):
        """Refresca la lista de voces disponibles en el sistema."""
        try:
            # NO reinicializar el motor TTS; solo recargar voces con engine actual
            # self.tts permanece igual, solo actualizamos el combo
            self.update_voice_list()
            
            # Actualizar la información de voces
            voices = self.tts.get_voices()
            voices_text = f"Voces disponibles ({len(voices)}):\n\n"
            for i, voice in enumerate(voices):
                voices_text += f"{i}. {voice.name}\n"
            
            # Buscar y actualizar el QLabel con información de voces
            config_tab = self.tabs.widget(1) if hasattr(self, 'tabs') else None
            if config_tab:
                # Buscar el label dentro del layout
                layout = config_tab.layout()
                if layout:
                    for i in range(layout.count()):
                        widget = layout.itemAt(i).widget()
                        if isinstance(widget, QLabel) and "Voces disponibles" in widget.text():
                            widget.setText(voices_text)
                            break
            
            self.status_label.setText(f"✓ Lista de voces refrescada ({len(voices)} disponibles)")
            QMessageBox.information(self, "Éxito", f"Se encontraron {len(voices)} voces.\n\nSi instalaste voces nuevas recientemente,\npuede ser necesario reiniciar Windows.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al refrescar voces: {e}")
            self.status_label.setText("Error al refrescar voces")

    
    def update_voice_list(self):
        """Actualiza la lista de voces disponibles."""
        voices = self.tts.get_voices()
        self.voice_combo.clear()
        for voice in voices:
            self.voice_combo.addItem(voice.name)
    
    def update_status(self):
        """Actualiza el estado de la aplicación."""
        # Sin barra de progreso: actualizamos la etiqueta de estado.
        if self.tts.is_speaking:
            self.status_label.setText("▶️ Leyendo...")
        else:
            # No sobreescribir mensajes de estado detallados
            if self.status_label.text() in ("▶️ Leyendo...", "⏸️ Pausado"):
                self.status_label.setText("Listo")


def main():
    """Punto de entrada de la aplicación."""
    app = QApplication(sys.argv)
    window = AITextReaderApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
