# 📖 Aplicación deA Síntesis de Voz

Una aplicación de escritorio offline para **leer en voz alta** documentos, imágenes e incluso el contenido de la pantalla. Ideal para accesibilidad, productividad y lectura asistida.

## ✨ Características

- 📄 **Soporta múltiples formatos**:
  - Documentos: PDF, Word (.doc, .docx), Texto plano (.txt)
  - Imágenes: JPG, PNG, BMP, TIFF, GIF (con OCR)
  - PowerPoint (.pptx)

- 🎤 **Síntesis de voz offline**:
  - Funciona sin conexión a internet
  - Múltiples voces disponibles
  - Control de velocidad (50-300 ppm)
  - Control de volumen

- ⏸️ **Controles de reproducción**:
  - ▶️ Reproducir
  - ⏸️ Pausar
  - ▶️ Reanudar desde la posición pausada
  - ⏹️ Detener

- 🖥️ **Lectura de pantalla**:
  - Captura y lee el contenido actual de la pantalla
  - OCR para extraer texto de imágenes en tiempo real

- ⚙️ **Configuración personalizable**:
  - Velocidad de lectura ajustable
  - Volumen regulable
  - Selección de voz

- 🇪🇸 **Soporte multiidioma**:
  - Español
  - Inglés
  - Francés
  - Alemán

## 🚀 Instalación

### Requisitos previos

- Python 3.8 o superior
- pip
- Windows, Linux o macOS

### Instalación en Windows

1. **Descargar Tesseract OCR** (necesario para OCR):
   - Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
   - Ejecutar el instalador
   - Instalar en la ruta por defecto o recordar la ruta de instalación

2. **Clonar el repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd "modelo ia lector"
   ```

3. **Crear entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar Tesseract** (si es necesario):
   ```bash
   # Editar main.py y agregar la línea (después de los imports):
   # import pytesseract
   # pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

6. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

### Instalación en Linux (Ubuntu/Debian)

```bash
# Instalar Tesseract
sudo apt-get install tesseract-ocr

# Clonar y instalar
git clone <URL_DEL_REPOSITORIO>
cd "modelo ia lector"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Instalación en macOS

```bash
# Instalar Tesseract (usando Homebrew)
brew install tesseract

# Clonar y instalar
git clone <URL_DEL_REPOSITORIO>
cd "modelo ia lector"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## 📖 Uso

### Interfaz principal

La aplicación tiene tres pestañas principales:

#### 1. 📄 Leer Archivo
- Haz clic en **"📂 Abrir Archivo"** para seleccionar un documento o imagen
- El texto se extrae automáticamente y se muestra en el área de texto
- Usa los botones de reproducción para controlar la lectura

#### 2. 🖥️ Leer Pantalla
- Haz clic en **"📸 Capturar Pantalla"** para capturar el contenido actual
- La aplicación realiza OCR automáticamente
- El texto capturado aparece en el área de texto
- Puedes hacer clic en "Leer" para escuchar el contenido

#### 3. ⚙️ Configuración
- **Velocidad de lectura**: Ajusta entre 50-300 palabras por minuto
- **Volumen**: Controla el nivel de sonido (0-100%)
- **Voz**: Selecciona entre las voces disponibles en tu sistema

### Controles de reproducción

- **▶️ Leer**: Comienza a leer el texto desde el principio
- **⏸️ Pausar**: Pausa la reproducción en el punto actual
- **▶️ Reanudar**: Continúa la lectura desde donde se pausó
- **⏹️ Detener**: Detiene la lectura completamente

## 🏗️ Estructura del proyecto

```
modelo ia lector/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias de Python
├── setup.py               # Script de instalación
├── README.md              # Este archivo
└── src/
    ├── modules/
    │   ├── __init__.py
    │   ├── text_extractor.py    # Extracción de texto
    │   └── text_to_speech.py    # Síntesis de voz
    ├── ui/
    │   ├── __init__.py
    │   └── main_window.py       # Interfaz gráfica
    └── utils/
        └── __init__.py
```

## 🛠️ Desarrollo

### Requisitos para desarrollo

```bash
pip install -r requirements.txt
```

### Módulos principales

#### `text_extractor.py`
- **TextExtractor**: Extrae texto de múltiples formatos
- **ScreenReader**: Captura y lee el contenido de la pantalla

#### `text_to_speech.py`
- **TextToSpeech**: Motor de síntesis de voz con controles

#### `main_window.py`
- **AITextReaderApp**: Aplicación principal con interfaz PyQt5
- **SpeechWorker**: Worker para síntesis de voz en hilo separado

## 🐛 Solución de problemas

### "pytesseract.TesseractNotFoundError"
- **Solución**: Instala Tesseract OCR siguiendo las instrucciones arriba

### No se extrae texto de imágenes
- Verifica que Tesseract esté instalado correctamente
- Intenta capturar una imagen de prueba simple primero

### Errores de PyQt5
- En algunos sistemas Linux, puede ser necesario: `sudo apt-get install python3-pyqt5`

### La síntesis de voz no funciona
- En Linux, instala: `sudo apt-get install espeak espeak-ng`
- En Windows/Mac, el motor debería funcionar de inmediato

## 📝 Notas

- La aplicación **funciona sin conexión a internet** después de la instalación inicial
- La pausa y reanudación requiere que la síntesis de voz se reinicie en Windows
- El OCR funciona mejor con texto impreso legible; el texto manuscrito puede no ser reconocido

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, abre primero un issue para discutir qué deseas cambiar.

## 📧 Contacto

Para reportar bugs o sugerencias, abre un issue en el repositorio.

---

**Hecho con ❤️ para mejorar la accesibilidad**
