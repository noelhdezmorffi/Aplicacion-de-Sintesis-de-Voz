# 📁 Estructura del Proyecto - Lector IA

```
modelo ia lector/
│
├── 📄 Archivos de Configuración
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── setup.py                # Script de instalación con setuptools
│   ├── requirements.txt         # Dependencias de Python
│   ├── setup_tesseract.py      # Configuración automática de Tesseract
│   └── .gitignore              # Archivos ignorados en Git
│
├── 📖 Documentación
│   ├── README.md               # Documentación principal
│   ├── QUICKSTART.md           # Guía de inicio rápido
│   ├── CHANGELOG.md            # Historial de cambios
│   ├── LICENSE                 # Licencia MIT
│   └── PROJECT_STRUCTURE.md    # Este archivo
│
├── 🚀 Scripts de Ejecución
│   ├── run.bat                 # Ejecutar en Windows
│   ├── run.sh                  # Ejecutar en Linux/Mac
│   ├── install.bat             # Instalar en Windows
│   └── install.sh              # Instalar en Linux/Mac
│
├── 🧪 Desarrollo y Pruebas
│   ├── test.py                 # Script de pruebas del sistema
│   ├── examples.py             # Ejemplos de uso de los módulos
│   └── .vscode/
│       └── settings.json       # Configuración para VS Code
│
└── 📦 src/ (Código Fuente)
    │
    ├── config.py               # Configuración global de la aplicación
    │
    ├── modules/                # Módulos principales
    │   ├── __init__.py
    │   ├── text_extractor.py   # Extracción de texto de archivos e imágenes
    │   │   ├── TextExtractor   # Clase principal para extracción
    │   │   └── ScreenReader    # Lectura de contenido de pantalla
    │   │
    │   └── text_to_speech.py   # Síntesis de voz
    │       ├── VoiceEngine     # Enumeración de motores
    │       └── TextToSpeech    # Clase de síntesis de voz
    │
    ├── ui/                     # Interfaz de Usuario (GUI)
    │   ├── __init__.py
    │   └── main_window.py      # Ventana principal con PyQt5
    │       ├── AITextReaderApp # Aplicación principal
    │       └── SpeechWorker    # Worker para síntesis de voz en hilo
    │
    └── utils/                  # Funciones Auxiliares
        ├── __init__.py
        └── helpers.py          # Funciones de apoyo (validación, etc.)
```

## 📊 Descripción de Componentes

### 🔐 Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `main.py` | Punto de entrada que inicia la aplicación |
| `setup.py` | Permite instalar la aplicación con `pip install .` |
| `requirements.txt` | Lista de dependencias de Python |
| `setup_tesseract.py` | Configura automáticamente Tesseract OCR |

### 📚 Módulos Principales

#### `text_extractor.py`
- **TextExtractor**: Extrae texto de múltiples formatos
  - PDF (PyPDF2)
  - Word (.doc, .docx) (python-docx)
  - PowerPoint (.pptx) (python-pptx)
  - Imágenes (pytesseract + Tesseract)
  - Texto plano (.txt)

- **ScreenReader**: Lee contenido de la pantalla
  - Captura de pantalla (mss)
  - OCR en tiempo real

#### `text_to_speech.py`
- **TextToSpeech**: Motor de síntesis de voz
  - Conversión de texto a voz (pyttsx3)
  - Control de velocidad y volumen
  - Soporte para múltiples voces
  - Ejecución en hilos separados

#### `main_window.py`
- **AITextReaderApp**: Interfaz gráfica principal
  - 3 pestañas: Archivos, Pantalla, Configuración
  - Controles de reproducción (Play, Pause, Resume, Stop)
  - Configuración en tiempo real

- **SpeechWorker**: Worker para síntesis asincrónica
  - Evita bloqueos de la interfaz
  - Manejo de errores

### 🛠️ Utilidades

#### `helpers.py`
- `get_supported_formats()`: Formatos soportados
- `validate_file()`: Validación de archivos
- `get_file_size_mb()`: Tamaño de archivo
- `truncate_text()`: Limitar longitud de texto

## 🔄 Flujo de la Aplicación

```
Usuario abre la aplicación (main.py)
    ↓
Interfaz gráfica (main_window.py)
    ↓
El usuario carga un archivo/captura pantalla
    ↓
TextExtractor extrae el texto
    ↓
El texto se muestra en la interfaz
    ↓
El usuario hace clic en "Leer"
    ↓
SpeechWorker ejecuta TextToSpeech en otro hilo
    ↓
La voz se reproduce sin bloquear la interfaz
    ↓
Usuario puede pausar, reanudar o detener
```

## 📦 Dependencias Principales

### Procesamiento de Archivos
- `PyPDF2`: Lectura de archivos PDF
- `python-docx`: Lectura de documentos Word
- `python-pptx`: Lectura de presentaciones PowerPoint
- `Pillow`: Procesamiento de imágenes

### OCR y Visión Computacional
- `pytesseract`: Interfaz Python para Tesseract OCR
- `mss`: Captura de pantalla

### Síntesis de Voz
- `pyttsx3`: Síntesis de voz offline

### Interfaz Gráfica
- `PyQt5`: Framework GUI

## 🎯 Funcionalidades Implementadas

✅ Extracción de texto de múltiples formatos
✅ OCR en imágenes (Tesseract)
✅ Lectura de pantalla en tiempo real
✅ Síntesis de voz offline (pyttsx3)
✅ Controles de reproducción (Play, Pause, Resume, Stop)
✅ Interfaz gráfica moderna (PyQt5)
✅ Configuración de velocidad y volumen
✅ Selección de voces
✅ Soporte multiidioma (Español, Inglés, Francés, Alemán)
✅ Documentación completa
✅ Scripts de instalación automática
✅ Ejemplos de uso
✅ Script de pruebas

## 🚀 Próximas Mejoras

- [ ] Base de datos para historial
- [ ] Búsqueda y reemplazo en el texto
- [ ] Temas personalizables (claro/oscuro)
- [ ] Atajos de teclado personalizables
- [ ] Soporte para eBooks (EPUB, MOBI)
- [ ] Sistema de plugins
- [ ] Exportación de audio
- [ ] Corrector ortográfico integrado

---

**Última actualización**: 8 de Diciembre, 2024
