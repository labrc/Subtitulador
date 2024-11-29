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

