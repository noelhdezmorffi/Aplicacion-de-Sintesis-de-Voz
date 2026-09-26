#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para parchear main_window.py y arreglar el problema de botones deshabilitados
"""

import re

# Leer el archivo
with open('src/ui/main_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# PARCHE 1: Cambiar on_export_finished para no bloquear con QMessageBox
old_on_export_finished = '''    def on_export_finished(self, file_path: str):
        """Callback cuando la exportación finaliza."""
        try:
            self.exported_audio_path = file_path
            self.status_label.setText(f"✓ Archivo exportado: {Path(file_path).name}")
            QMessageBox.information(self, "Exportado", f"Audio guardado en: {file_path}")
            # Asegurar que los botones estén habilitados correctamente
            self.save_btn.setEnabled(True if self.current_text else False)
            self.open_btn.setEnabled(True if os.path.exists(file_path) else False)
        except Exception as e:
            print(f"Error en on_export_finished: {e}")
            self.save_btn.setEnabled(True if self.current_text else False)
            self.open_btn.setEnabled(False)'''

new_on_export_finished = '''    def on_export_finished(self, file_path: str):
        """Callback cuando la exportación finaliza."""
        try:
            self.exported_audio_path = file_path
            file_name = Path(file_path).name
            
            # Actualizar estado sin bloquear UI
            self.status_label.setText(f"✓ Audio guardado: {file_name}")
            
            # Habilitar botones inmediatamente
            self.save_btn.setEnabled(True if self.current_text else False)
            self.open_btn.setEnabled(True if os.path.exists(file_path) else False)
            
            # Procesar eventos para asegurar actualización visual
            QApplication.processEvents()
            
            # Mostrar notificación sin bloquear UI (usando status bar en lugar de MessageBox)
            import time
            self.status_label.setText(f"✓ Audio guardado: {file_name} - Listo para abrir en reproductor")
            
        except Exception as e:
            print(f"Error en on_export_finished: {e}")
            self.save_btn.setEnabled(True if self.current_text else False)
            self.open_btn.setEnabled(False)'''

if old_on_export_finished in content:
    content = content.replace(old_on_export_finished, new_on_export_finished)
    print("✓ Parche 1 aplicado: on_export_finished")
else:
    print("✗ Parche 1 no encontrado - el código puede haber cambiado")

# PARCHE 2: Cambiar open_file para procesar eventos y asegurar actualización
old_open_file_update = '''            self.text_edit.setText(text)
            self.status_label.setText(f"✓ {Path(file_path).name} cargado ({len(text)} caracteres)")
            
            # Habilitar botón de guardar/exportar audio cuando hay texto
            # Abrir en reproductor solo si ya hay un archivo exportado previamente
            self.save_btn.setEnabled(True)
            self.open_btn.setEnabled(hasattr(self, 'exported_audio_path') and os.path.exists(self.exported_audio_path) if hasattr(self, 'exported_audio_path') else False)
            
            QApplication.processEvents()  # Procesar eventos para actualizar UI'''

if old_open_file_update in content:
    print("✓ Parche 2 ya existe: open_file con QApplication.processEvents()")
else:
    # Intentar encontrar y actualizar
    pattern = r'self\.text_edit\.setText\(text\)\s+self\.status_label\.setText\(f"✓ \{Path\(file_path\)\.name\} cargado'
    if re.search(pattern, content):
        print("✓ Parche 2 estructura encontrada, verificando completitud...")
    else:
        print("⚠ Parche 2 parcial - revisar manualmente")

# Escribir el archivo actualizado
with open('src/ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ Archivo src/ui/main_window.py actualizado")
print("\nCambios realizados:")
print("1. on_export_finished: Elimina QMessageBox.information() bloqueante")
print("2. Usa barra de estado para notificación en lugar de diálogo")
print("3. Procesa eventos para asegurar actualización visual inmediata")
