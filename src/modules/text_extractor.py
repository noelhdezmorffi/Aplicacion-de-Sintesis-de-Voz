"""
Módulo para extracción de texto de archivos PDF, documentos Word, PowerPoint e imágenes.

"""
import os
from pathlib import Path
from typing import Optional
import pytesseract
from PIL import Image
import PyPDF2
from docx import Document

# Configurar ruta de Tesseract (opcional - puede no existir en algunos sistemas)
TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
]
for tesseract_path in TESSERACT_PATHS:
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.pytesseract_cmd = tesseract_path
        break


class TextExtractor:
    """Extrae texto de múltiples formatos de archivo."""
    
    def __init__(self):
        """Inicializa el extractor con las rutas necesarias."""
        self.supported_formats = {
            '.pdf': self.extract_from_pdf,
            '.doc': self.extract_from_docx,
            '.docx': self.extract_from_docx,
            '.jpg': self.extract_from_image,
            '.jpeg': self.extract_from_image,
            '.png': self.extract_from_image,
            '.bmp': self.extract_from_image,
            '.tiff': self.extract_from_image,
            '.tif': self.extract_from_image,
            '.gif': self.extract_from_image,
            '.txt': self.extract_from_text,
            '.pptx': self.extract_from_pptx,
        }
        self.max_file_size = 100 * 1024 * 1024  # 100 MB
    
    def extract_text(self, file_path: str) -> Optional[str]:
        """
        Extrae texto de un archivo.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Texto extraído o None si hay error
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
            
            # Verificar tamaño
            file_size = file_path.stat().st_size
            if file_size > self.max_file_size:
                raise ValueError(f"Archivo demasiado grande: {file_size / 1024 / 1024:.2f}MB (máximo: 100MB)")
            
            ext = file_path.suffix.lower()
            
            if ext not in self.supported_formats:
                raise ValueError(f"Formato no soportado: {ext}")
            
            extractor_func = self.supported_formats[ext]
            text = extractor_func(str(file_path))
            
            if not text or len(text.strip()) == 0:
                raise ValueError("No se pudo extraer texto del archivo. El archivo puede estar vacío o en un formato no soportado.")
            
            return text
        
        except Exception as e:
            print(f"Error extrayendo texto: {e}")
            return None
    
    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """Extrae texto de un archivo PDF."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"--- Página {page_num + 1} ---\n"
                            text += page_text + "\n"
                    except Exception as e:
                        print(f"Error extrayendo página {page_num}: {e}")
        except Exception as e:
            print(f"Error al leer PDF: {e}")
        
        return text.strip()
    
    @staticmethod
    def extract_from_docx(file_path: str) -> str:
        """Extrae texto de archivos Word (.docx y .doc)."""
        try:
            # Intenta abrir como .docx primero
            doc = Document(file_path)
            text = ""
            
            # Extraer párrafos
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"
            
            # Extraer tablas
            for table in doc.tables:
                for row in table.rows:
                    row_text = " ".join(
                        cell.text.strip() for cell in row.cells
                    )
                    if row_text:
                        text += row_text + "\n"
            
            return text.strip() if text.strip() else ""
        except Exception as e:
            print(f"Error al leer documento Word: {e}")
            return ""
    
    @staticmethod
    def extract_from_pptx(file_path: str) -> str:
        """Extrae texto de archivos PowerPoint."""
        try:
            from pptx import Presentation
            
            presentation = Presentation(file_path)
            text = ""
            
            for slide_num, slide in enumerate(presentation.slides, 1):
                text += f"--- Diapositiva {slide_num} ---\n"
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text.strip():
                        text += shape.text + "\n"
            
            return text.strip()
        except ImportError:
            print("Módulo python-pptx no instalado")
            return ""
        except Exception as e:
            print(f"Error al leer PowerPoint: {e}")
            return ""
    
    @staticmethod
    def extract_from_image(file_path: str) -> str:
        """Extrae texto de una imagen usando OCR (Tesseract si está disponible)."""
        try:
            image = Image.open(file_path)
            
            # Mejorar imagen para mejor OCR
            image = image.convert('RGB')
            
            try:
                # Intentar OCR con pytesseract
                text = pytesseract.image_to_string(image, lang='spa+eng')
                return text.strip() if text.strip() else ""
            except Exception as ocr_error:
                print(f"OCR no disponible ({ocr_error}). Tesseract puede no estar instalado.")
                return ""
        except Exception as e:
            print(f"Error al abrir imagen: {e}")
            return ""
    
    @staticmethod
    def extract_from_text(file_path: str) -> str:
        """Extrae texto de un archivo de texto plano."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error al leer archivo de texto: {e}")
            return ""


class ScreenReader:
    """Lee el texto que se muestra en la pantalla."""
    
    @staticmethod
    def capture_screen_text() -> str:
        """
        Captura texto de la pantalla actual usando OCR.
        
        Returns:
            Texto capturado de la pantalla
        """
        try:
            from mss import mss
            
            with mss() as sct:
                # Captura el monitor principal
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                # Convierte a imagen PIL
                image = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                # Aplicar OCR
                text = pytesseract.image_to_string(image, lang='spa+eng')
                return text.strip()
        
        except ImportError:
            print("Módulo mss no instalado")
            return ""
        except Exception as e:
            print(f"Error al capturar pantalla: {e}")
            return ""
