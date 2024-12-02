# Subtitulador con GUI en Tkinter
Script GUI de auto-subtitulado basado en **Tkinter**, utiliza el modelo **Whisper** y **StableTS**. Obtené transcripciones y subtiutlados IA gratuitos en tu PC de corriendo este script de forma local.

## Características principales
- **Interfaz gráfica amigable**: Usa Tkinter para seleccionar archivos de entrada y salida, y configurar parámetros.
- **Compatibilidad con modelos preentrenados**: Soporte para los modelos **Whisper** de tamaños `tiny`, `base`, `small`, `medium` y `large`.
- **Opciones de transcripción avanzadas**: 
  - Generación de timestamps a nivel de segmentos o palabras.
  - Configuración personalizada de duración mínima y tags de estilo HTML para marcar palabras en los timestamps.
  - Opciones para generar archivos `.srt` o `.vtt` automáticamente según el archivo de entrada.
- **Soporte multilenguaje**: Detecta automáticamente el idioma del audio o permite configurarlo manualmente.
- **Salida automatizada**: Opcionalmente abre el archivo transcrito al finalizar.

## Requisitos
1. **Python** `>=3.8`
2. **Dependencias**
   ```plaintext
   torch==2.1.2+cu118 --index-url https://download.pytorch.org/whl/cu118
   stable-whisper==2.0.0
   stable-ts==1.0.0
   tkinter
## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/labrc/Subtitulador.git
   cd Subtitulador
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Asegúrate de tener FFmpeg instalado si planeas trabajar con formatos no estándar:
   - **En Linux**: 
     ```bash
     sudo apt install ffmpeg
     ```
   - **En Windows**: Descarga desde [FFmpeg.org](https://ffmpeg.org/download.html) y agrégalo al `PATH`.

## Uso
1. Ejecuta la aplicación:
   ```bash
   python subtitulos.py
   ```
2. Usa la interfaz para:
   - Seleccionar un archivo de audio de entrada.
   - Configurar opciones como modelo, idioma y parámetros avanzados.
   - Especificar la ubicación de salida o usar el nombre predeterminado.
3. Haz clic en **Convertir** y espera a que la transcripción se complete. Si activaste la opción, el archivo se abrirá automáticamente al finalizar.

## Capturas de Pantalla
*(Pronto imágenes de la GUI en funcionamiento.)*

## Contribuciones
Las contribuciones son bienvenidas. Si encuentras errores o deseas agregar nuevas funcionalidades, no dudes en abrir un *issue* o enviar un *pull request*.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
