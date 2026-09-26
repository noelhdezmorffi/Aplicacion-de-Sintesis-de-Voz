# ⚠️ SOLUCIÓN URGENTE - Python no encontrado

## El Problema
La consola dice: **"Python no está instalado o no está en el PATH"**

## La Solución Rápida

### Paso 1: Verificar si Python está instalado

Abre PowerShell y ejecuta:
```powershell
python --version
```

### Caso A: Si dice "python : No se reconoce..."

Python **NO está instalado**. Sigue estos pasos:

1. **Descarga Python**
   - Visita: https://www.python.org/downloads/
   - Descarga la versión **3.11** o superior

2. **Instala Python**
   - Ejecuta el instalador descargado
   - **⚠️ IMPORTANTE**: Al comenzar la instalación, marca la opción:
     ```
     ☑ Add Python 3.x to PATH
     ```
   - Haz clic en "Install Now"
   - Espera a que termine

3. **Reinicia tu computadora**
   - Esto es importante para que Windows reconozca Python

4. **Abre una NUEVA consola PowerShell**
   - Presiona `Win + X` → PowerShell
   - Verifica: `python --version`

5. **Ejecuta el instalador**
   ```powershell
   cd C:\Users\neutr\Desktop\proyectos\modelo ia lector
   .\install.bat
   ```

---

### Caso B: Si dice la versión de Python

Python **SÍ está instalado**, pero no se encontró durante la instalación.

Intenta:

1. **Abre una NUEVA consola PowerShell** (presiona Win + X)

2. **Navega a la carpeta**:
   ```powershell
   cd "C:\Users\neutr\Desktop\proyectos\modelo ia lector"
   ```

3. **Ejecuta nuevamente**:
   ```powershell
   .\install.bat
   ```

Si aún no funciona:

4. **Intenta instalación manual**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

---

## Alternativa: Verificación Manual

Si los pasos arriba no funcionan, ejecuta esto en PowerShell:

```powershell
# 1. Verificar dónde está Python
where python

# 2. Si encuentra algo, anota la ruta
# 3. Si NO encuentra nada, Python no está en PATH

# 4. Intenta con py (alias de Windows)
py --version

# Si py funciona pero python no, crea un alias:
# Abre Bloc de notas como administrador
# Archivo: C:\Windows\py.cmd
# Contenido:
# @echo off
# python %*

```

---

## ✅ Verificación Final

Cuando Python esté correctamente instalado, verifica:

```powershell
python --version
# Debería mostrar: Python 3.11.x (o superior)

python -c "import sys; print(sys.executable)"
# Debería mostrar la ruta a Python
```

---

## 🆘 Si Nada Funciona

1. **Desinstala Python completamente**
   - Panel de Control → Programas → Desinstalar
   - Busca "Python 3.x"
   - Desinstala

2. **Reinicia tu computadora**

3. **Descarga e instala nuevamente**
   - https://www.python.org/downloads/
   - Version 3.11 o superior
   - **MARCA "Add Python to PATH"**

4. **Reinicia nuevamente**

5. **Intenta nuevamente**

---

## 📞 Otra Opción: Instalación Manual

Si el instalador sigue sin funcionar, hazlo manualmente:

```powershell
# 1. Abre PowerShell en la carpeta del proyecto
cd "C:\Users\neutr\Desktop\proyectos\modelo ia lector"

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
.\venv\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install --upgrade pip
pip install PyQt5 pyttsx3 PyPDF2 python-docx Pillow pytesseract python-pptx mss

# 5. Ejecutar la aplicación
python main.py
```

---

## 🎯 Próximos Pasos Después de Instalar Python

1. Ejecuta: `check_python.bat` (para verificar)
2. Ejecuta: `install.bat` (para instalar dependencias)
3. Descarga Tesseract OCR desde: https://github.com/UB-Mannheim/tesseract/wiki
4. Ejecuta: `run.bat` (para iniciar la aplicación)

---

**¡Avísame cuando hayas instalado Python y volveremos a intentar!** 👍
