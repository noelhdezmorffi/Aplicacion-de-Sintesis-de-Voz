"""
Funciones auxiliares para la aplicación.
"""

import os
from pathlib import Path
from typing import List


def get_supported_formats() -> dict:
    """Retorna los formatos soportados organizados por categoría."""
    return {
        "Documentos": [".pdf", ".doc", ".docx", ".txt", ".pptx"],
        "Imágenes": [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"],
    }


def get_format_description() -> str:
    """Retorna una descripción de los formatos soportados."""
    formats = get_supported_formats()
    desc = "Formatos soportados:\n\n"
    
    for category, exts in formats.items():
        desc += f"{category}: {', '.join(exts).upper()}\n"
    
    return desc


def validate_file(file_path: str) -> tuple[bool, str]:
    """
    Valida que el archivo exista y sea de un formato soportado.
    
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    path = Path(file_path)
    
    if not path.exists():
        return False, f"Archivo no encontrado: {file_path}"
    
    supported = []
    for exts in get_supported_formats().values():
        supported.extend(exts)
    
    if path.suffix.lower() not in supported:
        return False, f"Formato no soportado: {path.suffix}\n\n{get_format_description()}"
    
    return True, ""


def get_file_size_mb(file_path: str) -> float:
    """Retorna el tamaño del archivo en MB."""
    return Path(file_path).stat().st_size / (1024 * 1024)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Trunca texto si es muy largo."""
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def get_resource_path(relative_path: str) -> str:
    """Obtiene la ruta absoluta de un recurso."""
    base_path = Path(__file__).parent.parent
    return str(base_path / relative_path)
