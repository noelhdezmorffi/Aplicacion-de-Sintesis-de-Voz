"""
[TEMPORAL] Contenedor de patching para main_window.py
Este archivo contiene los métodos corregidos que serán aplicados a main_window.py
"""

# Parche para on_export_finished: no bloquear con QMessageBox
def on_export_finished_patched(self, file_path: str):
    """Callback cuando la exportación finaliza."""
    try:
        self.exported_audio_path = file_path
        file_name = Path(file_path).name
        
        # Actualizar estado sin bloquear UI
        self.status_label.setText(f"✓ Audio guardado: {file_name}")
        
        # Habilitar botones inmediatamente
        self.save_btn.setEnabled(True if self.current_text else False)
        self.open_btn.setEnabled(True if os.path.exists(file_path) else False)
        
        # Procesar eventos para actualizar UI
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        
        # Mostrar mensaje sin bloquear (no-modal)
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Éxito")
        msg.setText(f"Audio guardado en:\n{file_path}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        # No bloquear: no llamar a exec_()
        
    except Exception as e:
        print(f"Error en on_export_finished: {e}")
        self.save_btn.setEnabled(True if self.current_text else False)
        self.open_btn.setEnabled(False)

# Parche para open_file: asegurar que botones se actualicen correctamente
def open_file_patched(self):
    """Abre un diálogo para seleccionar archivo."""
    from PyQt5.QtWidgets import QApplication
    
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
        QApplication.processEvents()  # Actualizar UI inmediatamente
        
        # Extraer texto
        text = self.text_extractor.extract_text(file_path)
        
        if text:
            self.current_text = text
            self.current_file = file_path
            self.is_paused = False
            self.pause_position = 0
            
            # No hay botones de reproducción o barra de progreso
            
            self.text_edit.setText(text)
            self.status_label.setText(f"✓ {Path(file_path).name} cargado ({len(text)} caracteres)")
            
            # Habilitar botón de guardar/exportar audio cuando hay texto
            # Abrir en reproductor solo si ya hay un archivo exportado previamente
            self.save_btn.setEnabled(True)
            self.open_btn.setEnabled(hasattr(self, 'exported_audio_path') and os.path.exists(self.exported_audio_path) if hasattr(self, 'exported_audio_path') else False)
            
            QApplication.processEvents()  # Procesar eventos para actualizar UI
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "No se pudo extraer texto del archivo.")
            self.status_label.setText("Error al extraer texto")
            self.save_btn.setEnabled(False)
            self.open_btn.setEnabled(False)
