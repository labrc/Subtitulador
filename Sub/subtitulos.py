import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import stable_whisper



def convert_audio():
    input_path = input_entry.get()
    output_path = output_entry.get() if (output_checkbox_var.get() ==  False) else f"{input_path.rsplit('.', 1)[0]}.srt"
    model_name = model_var.get()
    language = language_var.get()
    word_timestamps = timestamps_var.get()
    temperature = temperature_var.get()
    max_initial_timestamp = float(fragment_sep_entry.get() or 0)

    # Opciones avanzadas
    beam_size = int(beam_size_entry.get() or 5)
    batch_size = int(batch_size_entry.get() or 16)
    suppress_tokens = suppress_tokens_entry.get()
    compression_ratio_threshold = float(compression_ratio_entry.get() or 2.5)

    try:
        tag_value = tag_entry.get()

           # Asegúrate de evaluar la cadena como una tupla
        tag_tuple = eval(tag_value)  # Evalúa la cadena y la convierte en tupla
        model = stable_whisper.load_model(model_name)
        result = model.transcribe(
            input_path,
            language=language if language != "Auto" else None,
            word_timestamps=word_timestamps,
            temperature=temperature,
            max_initial_timestamp=max_initial_timestamp,
            beam_size=beam_size,
            
            suppress_tokens=suppress_tokens,
            compression_ratio_threshold=compression_ratio_threshold,
        )
        result.to_srt_vtt(
            output_path,
            segment_level=segment_level_var.get() ,
            word_level=word_level_var.get(),
            min_dur=min_dur_var.get(),
            tag=tag_tuple,
            vtt=vtt_var.get(),
            reverse_text=reverse_text_var.get(),
            )
        
        
        status_label.config(text="Conversión exitosa", fg="green")
        if abrir_despues_var.get():
            os.startfile(output_path)  # En Windows
    except Exception as e:
        status_label.config(text=f"Hubo un problema: {str(e)}", fg="red")

def browse_input():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.m4a")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def browse_output():
    file_path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT Files", "*.srt")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)

# Crear ventana principal
root = tk.Tk()
root.title("Transcriptor de Audio")
root.geometry("720x620")  # Ancho ajustado para acomodar dos columnas

# Entrada y salida de archivos
frame_paths = tk.Frame(root)
frame_paths.pack(pady=5)

tk.Label(frame_paths, text="Archivo de Entrada:").grid(row=0, column=0, padx=5, pady=2)
input_entry = tk.Entry(frame_paths, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=2)
browse_input_btn = tk.Button(frame_paths, text="Explorar", command=browse_input)
browse_input_btn.grid(row=0, column=2, padx=5, pady=2)

output_checkbox_var = tk.BooleanVar(value=True)
output_checkbox = tk.Checkbutton(frame_paths, text="Usar misma carpeta/nombre para salida", variable=output_checkbox_var)
output_checkbox.grid(row=1, column=1, columnspan=2, pady=2)

tk.Label(frame_paths, text="Archivo de Salida:").grid(row=2, column=0, padx=5, pady=2)
output_entry = tk.Entry(frame_paths, width=50, state=tk.DISABLED)
output_entry.grid(row=2, column=1, padx=5, pady=2)
browse_output_btn = tk.Button(frame_paths, text="Explorar", command=browse_output, state=tk.DISABLED)
browse_output_btn.grid(row=2, column=2, padx=5, pady=2)

# Habilitar/deshabilitar la entrada de salida
def toggle_output_entry():
    state = tk.NORMAL if not output_checkbox_var.get() else tk.DISABLED
    output_entry.config(state=state)
    browse_output_btn.config(state=state)

output_checkbox.config(command=toggle_output_entry)

# Selección de configuración
frame_settings = tk.LabelFrame(root, text="Configuraciones Básicas")
frame_settings.pack(fill="x", padx=10, pady=0)

# Primera columna de configuraciones básicas
frame_left = tk.Frame(frame_settings)
frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

tk.Label(frame_left, text="Modelo:").grid(row=0, column=0, padx=5, pady=5)
model_var = tk.StringVar(value="medium")
model_dropdown = ttk.Combobox(frame_left, textvariable=model_var, values=["tiny", "base", "small", "medium", "large"], state="readonly")
model_dropdown.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_left, text="Idioma:").grid(row=1, column=0, padx=5, pady=5)
language_var = tk.StringVar(value="es")
language_dropdown = ttk.Combobox(frame_left, textvariable=language_var, values=["Auto", "en", "es", "fr", "de", "it"], state="readonly")
language_dropdown.grid(row=1, column=1, padx=5, pady=5)

timestamps_var = tk.BooleanVar(value=False)
timestamps_checkbox = tk.Checkbutton(frame_left, text="Habilitar Timestamps por palabra", variable=timestamps_var)
timestamps_checkbox.grid(row=2, column=0, columnspan=2, pady=5)

tk.Label(frame_left, text="Temperatura:").grid(row=3, column=0, padx=5, pady=5)
temperature_var = tk.DoubleVar(value=0.5)
temperature_slider = tk.Scale(frame_left, variable=temperature_var, from_=0, to=1, resolution=0.1, orient="horizontal")
temperature_slider.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_left, text="Separación de Fragmentos:").grid(row=4, column=0, padx=5, pady=5)
fragment_sep_entry = tk.Entry(frame_left, width=10)
fragment_sep_entry.grid(row=4, column=1, padx=5, pady=5)

# Segunda columna de configuraciones adicionales
frame_right = tk.Frame(frame_settings)
frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

tk.Label(frame_right, text="Segment-level Timestamps:").grid(row=0, column=0, padx=5, pady=5)
segment_level_var = tk.BooleanVar(value=True)
segment_level_checkbox = tk.Checkbutton(frame_right, text="Habilitar", variable=segment_level_var)
segment_level_checkbox.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_right, text="Word-level Timestamps:").grid(row=1, column=0, padx=5, pady=5)
word_level_var = tk.BooleanVar(value=True)
word_level_checkbox = tk.Checkbutton(frame_right, text="Habilitar", variable=word_level_var)
word_level_checkbox.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_right, text="Duración Mínima (s):").grid(row=2, column=0, padx=5, pady=5)
min_dur_var = tk.DoubleVar(value=0.2)
min_dur_entry = tk.Entry(frame_right, textvariable=min_dur_var, width=10)
min_dur_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_right, text="Tag Inicio/Fin:").grid(row=3, column=0, padx=5, pady=5)
tag_entry = tk.Entry(frame_right, width=40)
tag_entry.insert(0, "('<font color=\"#00ff00\">', '</font>')")
tag_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_right, text="Formato VTT:").grid(row=4, column=0, padx=5, pady=5)
vtt_var = tk.BooleanVar(value=False)
vtt_checkbox = tk.Checkbutton(frame_right, text="Habilitar", variable=vtt_var)
vtt_checkbox.grid(row=4, column=1, padx=5, pady=5)

tk.Label(frame_right, text="Texto Invertido:").grid(row=5, column=0, padx=5, pady=0)
reverse_text_var = tk.BooleanVar(value=False)
reverse_text_checkbox = tk.Checkbutton(frame_right, text="Habilitar", variable=reverse_text_var)
reverse_text_checkbox.grid(row=5, column=1, padx=5, pady=0)

# Botón de convertir
#convert_btn = tk.Button(root, text="Convertir", command=convert_audio)
#convert_btn.pack(pady=10)
abrir_despues_var = tk.BooleanVar(value=False)
abrir_despues_var = tk.BooleanVar(value=True)
abrir_despues_checkbox = tk.Checkbutton(frame_paths, text="Abrir al generar", variable=abrir_despues_var)
abrir_despues_checkbox.grid(pady=3)

# Etiqueta de estado
status_label = tk.Label(root, text="", fg="red")
status_label.pack(pady=3)
# Opciones avanzadas
frame_advanced = tk.LabelFrame(root, text="Opciones Avanzadas")
frame_advanced.pack(fill="x", padx=10, pady=0)

# Tamaño de beam
tk.Label(frame_advanced, text="Tamaño de Beam:").grid(row=0, column=0, padx=5, pady=5)
beam_size_entry = tk.Entry(frame_advanced, width=10)
beam_size_entry.insert(0, "5")
beam_size_entry.grid(row=0, column=1, padx=5, pady=5)

# Tamaño de batch
tk.Label(frame_advanced, text="Tamaño de Batch:").grid(row=1, column=0, padx=5, pady=5)
batch_size_entry = tk.Entry(frame_advanced, width=10)
batch_size_entry.insert(0, "16")
batch_size_entry.grid(row=1, column=1, padx=5, pady=5)

# Tokens a suprimir
tk.Label(frame_advanced, text="Tokens a Suprimir:").grid(row=2, column=0, padx=5, pady=5)
suppress_tokens_entry = tk.Entry(frame_advanced, width=20)
suppress_tokens_entry.grid(row=2, column=1, padx=5, pady=5)

# Umbral de compresión
tk.Label(frame_advanced, text="Umbral de Compresión:").grid(row=3, column=0, padx=5, pady=5)
compression_ratio_entry = tk.Entry(frame_advanced, width=10)
compression_ratio_entry.insert(0, "2.5")
compression_ratio_entry.grid(row=3, column=1, padx=5, pady=0)
# Etiqueta de estado
status_label = tk.Label(root, text="", fg="red")
status_label.pack(pady=5)
# Botón de convertir
convert_btn = tk.Button(root, text="Convertir", command=convert_audio)
convert_btn.pack(pady=10)

#tk.Label(pack, text="Texto Invertido:").grid(row=5, column=0, padx=5, pady=5)
tk.Label(frame_paths, text="Segment-level Timestamps:").grid(row=0, column=0, padx=5, pady=5)
#abrir_despues_checkbox.grid(row=1, column=1, padx=5, pady=5)



root.mainloop()
