# Guía: Instalar Voces SAPI5 Adicionales en Windows

Esta guía te muestra cómo instalar voces Text-to-Speech (TTS) adicionales en Windows para usar con la aplicación "Lector IA".

## ¿Qué es SAPI5?

SAPI5 (Speech API 5) es la plataforma de síntesis de voz nativa de Windows. Las voces instaladas aparecerán automáticamente en la aplicación.

---

## Opción 1: Microsoft Edge Voices (Recomendado - Gratis)

Microsoft ha incluido voces Neural de alta calidad en Edge desde Windows 11 (también disponibles en Windows 10 con actualizaciones).

### Pasos:

1. **Abre Configuración de Windows:**
   - Presiona `Win + I` para abrir Configuración.

2. **Accede a la sección de Voz:**
   - Navega a: `Configuración > Hora e idioma > Voz`

3. **Descarga voces adicionales:**
   - En la sección **"Voces"**, verás un botón **"+ Agregar voces"** o similar.
   - Haz clic para ver voces disponibles (en inglés, español, francés, alemán, etc.).
   - Selecciona una voz y haz clic en **"Descargar"** (pueden tardar 100-500 MB por voz).

4. **Las voces aparecerán en la app:**
   - Cierra y reabre la aplicación "Lector IA".
   - Abre la pestaña **"⚙️ Configuración"** → **"🎤 Voz"**.
   - Verifica que aparecen las nuevas voces en el desplegable.

---

## Opción 2: Microsoft Speech Platform (Windows 10/11)

Si la Opción 1 no funciona, puedes instalar voces desde Microsoft Speech Platform.

### Pasos:

1. **Descarga Microsoft Speech Platform Runtime:**
   - Ve a: [Microsoft Speech Platform - Runtime](https://www.microsoft.com/en-us/download/details.aspx?id=27224)
   - Descarga **"MSpeechTTSEngine.msi"** (motor de síntesis).
   - Ejecuta el instalador.

2. **Descarga paquetes de idioma:**
   - Ve a la misma página y busca **"Runtime Languages"**.
   - Descarga los idiomas que desees:
     - `Spanish_Spain-es-ES` (Español de España)
     - `English_US-en-US` (Inglés estadounidense)
     - `French_France-fr-FR` (Francés)
     - etc.
   - Ejecuta cada instalador `.msi`.

3. **Verifica la instalación:**
   - Abre **"Panel de Control"** → **"Sonido"** → **"Voz"**.
   - Deberías ver las nuevas voces listadas.

4. **Usa en la app:**
   - Reabre "Lector IA" y las voces aparecerán en **"🎤 Voz"**.

---

## Opción 3: Instalar Voces de Windows 11 en Windows 10

Windows 11 incluye voces Neural mejores. Puedes extraer esas voces en Windows 10.

### Pasos (avanzado):

1. **Accede a la carpeta de voces del sistema:**
   - Presiona `Win + R` y copia esta ruta:
     ```
     %AppData%\Microsoft\Speech\Voices\Tokens
     ```
   - Presiona Enter.

2. **Descarga voces Neural de Windows 11:**
   - Ve a: [GitHub - Windows 11 Neural TTS Voices](https://github.com/ranyitz/windows11-tts-voices)
   - Descarga el archivo `.zip` de voces que desees.

3. **Extrae las voces en la carpeta:**
   - Descomprime el `.zip`.
   - Copia las carpetas de voces a:
     ```
     C:\Users\[TuUsuario]\AppData\Roaming\Microsoft\Speech\Voices\Tokens
     ```

4. **Reinicia la app:**
   - Cierra y reabre "Lector IA".

---

## Opción 4: Voces Google Cloud TTS (En línea - Mejor calidad)

Si quieres voces de muy alta calidad, puedes usar Google Cloud TTS (requiere internet y cuenta gratuita).

### Pasos:

1. **Crea una cuenta en Google Cloud:**
   - Ve a: [Google Cloud Console](https://console.cloud.google.com/)
   - Regístrate (tienes créditos gratis).

2. **Habilita Text-to-Speech API:**
   - En el console, busca "Text-to-Speech API" y habilítala.

3. **Descarga credenciales:**
   - Crea una clave de servicio (Service Account Key) en formato JSON.
   - Guárdala en el proyecto.

4. **Instala el cliente de Google Cloud:**
   ```powershell
   pip install google-cloud-texttospeech
   ```

5. **Integración en "Lector IA":**
   - Puedo implementar esto si lo deseas (requiere modificar `text_to_speech.py`).

---

## Opción 5: eSpeak (Voces Abiertas Locales)

eSpeak es un motor TTS de código abierto que soporta múltiples idiomas y voces gratuitas.

### Pasos:

1. **Descarga eSpeak:**
   - Ve a: [eSpeak NG Download](https://github.com/espeak-ng/espeak-ng/releases)
   - Descarga el instalador Windows (`.exe` o `.msi`).

2. **Instala:**
   - Ejecuta el instalador y sigue los pasos.

3. **Configura pyttsx3 para usar eSpeak:**
   - Abre `src/modules/text_to_speech.py` en la app.
   - En `__init__`, cambia:
     ```python
     self.engine = pyttsx3.init()  # Usa motor por defecto
     ```
     a:
     ```python
     self.engine = pyttsx3.init('espeak')  # Usa eSpeak
     ```

4. **Reinicia la app:**
   - Las voces eSpeak aparecerán en el desplegable.

---

## Verificar Voces Instaladas

### En Windows:

1. **Panel de Control (método oficial):**
   - Abre **Panel de Control** → **Sonido** → **Voz** → **Cambiar idioma o voz**.
   - Verás todas las voces instaladas y activas.

2. **Con PowerShell (para desarrolladores):**
   - Abre PowerShell como administrador.
   - Ejecuta:
     ```powershell
     $obj = New-Object -ComObject SAPI.SPVoice
     $obj.GetVoices() | Select-Object Name
     ```

### En la app "Lector IA":

1. Abre la pestaña **"⚙️ Configuración"**.
2. Mira la sección **"Voces disponibles en el sistema"** (lista al pie).
3. O abre el desplegable **"🎤 Voz"** y verás todas las voces listadas.

---

## Refrescar la Lista de Voces en la App

Si instalas voces nuevas y no aparecen en la app:

1. **Cierra completamente la aplicación** "Lector IA".
2. **Reabre la aplicación:**
   - En Windows: ejecuta `run.bat` desde el directorio del proyecto.
   - O: `python main.py`.
3. **Abre la pestaña "⚙️ Configuración".**
4. **Haz clic en el botón "🔄 Refrescar voces"** (si disponible).
5. Las voces nuevas aparecerán en el desplegable **"🎤 Voz"**.

---

## Recomendaciones

### Para mejor calidad de audio:

1. **Combina opciones:**
   - Usa **Microsoft Edge Voices** (Opción 1) para voces Neural de calidad.
   - Prueba diferentes **Presets** en la pestaña Configuración:
     - **"Narrador"**: Para audiolibros (tono bajo, claro).
     - **"Anuncio"**: Para contenido dinámico (enérgico).
     - **"Suave"**: Para narrativa relajada.

2. **Ajusta velocidad y volumen:**
   - Experimenta con valores entre **100-200 ppm** (palabras por minuto).
   - Mantén volumen entre **0.7-1.0** según preferencia.

3. **Prueba antes de exportar:**
   - Usa el botón **"🔈 Probar voz"** para escuchar una muestra.
   - Ajusta presets hasta estar satisfecho.
   - Luego **"💾 Guardar audio"** y **"🔊 Abrir en reproductor"**.

---

## Solución de Problemas

### Las voces nuevas no aparecen en la app:

1. **Verifica la instalación:**
   - En Panel de Control → Sonido → Voz, ¿aparecen las nuevas voces?
   - Si no, la instalación no fue exitosa.

2. **Reinicia la app:**
   - Cierra completamente la app y reabre.
   - La app carga voces al iniciar.

3. **Reinicia Windows:**
   - A veces, cambios en SAPI5 requieren reinicio.

4. **Comprueba permisos:**
   - Asegúrate de que la carpeta `AppData\Roaming\Microsoft\Speech\Voices` es accesible.

### El audio suena mal o entrecortado:

1. **Reduce la velocidad:**
   - Baja el valor en **"⏱️ Velocidad de lectura"** (150-120 ppm).

2. **Aumenta volumen:**
   - Si es muy bajo, ajusta **"🔊 Volumen"** a 0.9-1.0.

3. **Cambia de voz:**
   - Algunas voces tienen mejor calidad. Prueba todas disponibles.

4. **Verifica recursos del sistema:**
   - TTS es intensivo. Cierra otras aplicaciones si hay lag.

---

## Preguntas Frecuentes

**¿Las voces nuevas cuestan dinero?**
- Las voces de Microsoft (Opción 1-2) son gratuitas con Windows.
- eSpeak (Opción 5) es código abierto y gratuito.
- Google Cloud (Opción 4) ofrece créditos gratuitos iniciales.

**¿Puedo usar voces de macOS o Linux en Windows?**
- No directamente. Pero puedes usar Google Cloud TTS que funciona en cualquier plataforma.

**¿Cuál es la mejor opción para audiolibros?**
- Microsoft Edge Voices (Opción 1) con preset "Narrador".
- O Google Cloud TTS (Opción 4) para máxima calidad.

**¿Se pueden crear voces personalizadas?**
- No con SAPI5 nativo. Requeriría TTS personalizado (p. ej., con Coqui TTS o modelos ML).

---

## Próximos Pasos

Después de instalar nuevas voces:

1. Reabre la app "Lector IA".
2. Abre **"⚙️ Configuración"**.
3. Selecciona una voz nueva en **"🎤 Voz"**.
4. Prueba con **"🔈 Probar voz"**.
5. Ajusta preset y velocidad según prefieras.
6. Carga un archivo (**"📂 Abrir Archivo"**) y **"💾 Guardar audio"**.
7. Abre el audio con **"🔊 Abrir en reproductor"** y disfruta.

---

## Contacto / Soporte

Si encuentras problemas al instalar voces:

1. Revisa los logs de Windows:
   - Panel de Control → Visor de eventos → Sistema.

2. Prueba en PowerShell (como admin):
   ```powershell
   Test-WindowsFeature Speech-Text-to-Speech
   ```

3. Si nada funciona, puedo integrar otra TTS (Google Cloud, Coqui, etc.) en la app.

---

**¡Espero que disfrutes con las nuevas voces! 🎙️**
