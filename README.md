# Subtitulador
Script de auto-subtitulado basado en Whissper/StableTS
Transcriptor de Audio con GUI en Tkinter
Este proyecto es una aplicación GUI (interfaz gráfica de usuario) desarrollada en Python, que utiliza el modelo Whisper mediante la biblioteca stable-whisper para transcribir archivos de audio a formatos como .srt o .vtt. La interfaz está diseñada con Tkinter, lo que la hace intuitiva y fácil de usar, incluso para personas sin experiencia técnica.

#Características principales
Interfaz gráfica amigable: Usa Tkinter para seleccionar archivos de entrada y salida, y configurar parámetros.
Compatibilidad con modelos preentrenados: Soporte para los modelos Whisper de tamaños tiny, base, small, medium y large.
Opciones de transcripción avanzadas:
Generación de timestamps a nivel de segmentos o palabras.
Configuración personalizada de duración mínima y tags de estilo HTML para marcar palabras en los timestamps.
Opciones para generar archivos .srt o .vtt automáticamente según el archivo de entrada.
Soporte multilenguaje: Detecta automáticamente el idioma del audio o permite configurarlo manualmente.
Salida automatizada: Opcionalmente abre el archivo transcrito al finalizar.
#Requisitos
Python >=3.8
Dependencias
torch==2.1.2+cu118 --index-url https://download.pytorch.org/whl/cu118
stable-whisper==2.0.0
stable-ts==1.0.0
tkinter
#Instalación
Clona el repositorio:
git clone https://github.com/tu-usuario/transcriptor-audio-tkinter.git
cd transcriptor-audio-tkinter
Instala las dependencias:
pip install -r requirements.txt
Asegúrate de tener FFmpeg instalado si planeas trabajar con formatos no estándar:
En Linux: sudo apt install ffmpeg
En Windows: Descarga desde FFmpeg.org y agrégalo al PATH.
#Uso
Ejecuta la aplicación:
python transcriptor_gui.py
Usa la interfaz para:
Seleccionar un archivo de audio de entrada.
Configurar opciones como modelo, idioma, y parámetros avanzados.
Especificar la ubicación de salida o usar el nombre predeterminado.
Haz clic en Convertir y espera a que la transcripción se complete. Si activaste la opción, el archivo se abrirá automáticamente al finalizar.
#Capturas de Pantalla
(Agrega aquí imágenes de la GUI en funcionamiento.)

#Contribuciones
Las contribuciones son bienvenidas. Si encuentras errores o deseas agregar nuevas funcionalidades, no dudes en abrir un issue o enviar un pull request.

#Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

