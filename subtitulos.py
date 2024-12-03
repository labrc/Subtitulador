import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import stable_whisper
import json

CONFIG_FILE = "config.json"

def save_config(config_data):
    serializable_config = {
        key: (value.get() if hasattr(value, "get") else value)
        for key, value in config_data.items()
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(serializable_config, file, indent=4)

def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            data = json.load(file)
            return {
                "input_path": data.get("input_path", ""),
                "output_path": data.get("output_path", ""),
                "model_name": data.get("model_name", "medium"),
                "language": data.get("language", "Auto"),
                "word_timestamps": tk.BooleanVar(value=data.get("word_timestamps", False)),
                "temperature": tk.DoubleVar(value=data.get("temperature", 0.5)),
                "max_initial_timestamp": data.get("max_initial_timestamp", 0.0),
                "beam_size": data.get("beam_size", 5),
                "batch_size": data.get("batch_size", 16),
                "suppress_tokens": data.get("suppress_tokens", ""),
                "compression_ratio_threshold": data.get("compression_ratio_threshold", 2.5),
                "segment_level": tk.BooleanVar(value=data.get("segment_level", True)),
                "word_level": tk.BooleanVar(value=data.get("word_level", True)),
                "tag": data.get("tag", "('<font color=\"#00ff00\">', '</font>')"),
                "vtt": tk.BooleanVar(value=data.get("vtt", False)),
                "reverse_text": tk.BooleanVar(value=data.get("reverse_text", False)),
            }
    except FileNotFoundError:
        print("Archivo de configuración no encontrado. Se usará configuración predeterminada.")
        return {}

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
    config = {
        "input_path": input_path,
        "output_path": output_path,
        "model_name": model_name,
        "language": language,
        "word_timestamps": word_timestamps,
        "temperature": temperature,
        "max_initial_timestamp": max_initial_timestamp,
        "beam_size": beam_size,
        "batch_size": batch_size,
        "suppress_tokens": suppress_tokens,
        "compression_ratio_threshold": compression_ratio_threshold,
        "segment_level": segment_level_var.get(),
        "word_level": word_level_var.get(),
        "tag": tag_entry,
        "vtt": vtt_var,
        "reverse_text": reverse_text_var,
    }
    save_config(config)

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
root.geometry("780x820")  # Ancho ajustado para acomodar dos columnas
root.resizable(False,False)
root.configure(bg="#00070d")
root.option_add("*Font", "Poppins 8") 
# Set popdown listbox styling via the option database
root.option_add('*TCombobox*Listbox.background', '#00070d')  # Background of the listbox
root.option_add('*TCombobox*Listbox.foreground', 'white')     # Text color in the listbox
root.option_add('*TCombobox*Listbox.selectBackground', '#d3d4d5')  # Selection background color
root.option_add('*TCombobox*Listbox.selectForeground', '#00070d')    # Selection text color




style = ttk.Style()
style.configure("TCombobox",
                arrowcolor="green",         # Color of the dropdown arrow
                arrowsize=20,               # Size of the dropdown arrow
                background="#0a1117",         # Background of the combobox entry
                foreground="white",        # Text color inside the combobox
                fieldbackground="gray1",    # Background color of the entry field
                insertcolor="white",       # Cursor color
                insertwidth=2,              # Width of the cursor
                selectbackground="yellow2", # Selection background color
                selectforeground="#00070d")   # Selection text color

# Colores para los estados del Combobox
style.map("TCombobox",
                   background=[('disabled', 'yellow2'),  # Fondo cuando está deshabilitado
                               ('active', 'yellow3')],    # Fondo cuando está activo (ratón encima)
                   foreground=[('disabled', 'green1')],
                    relief=[('pressed', '!disabled', 'sunken')])  # Color del texto cuando está deshabilitado

# style.configure("TButton",
                # font=("Poppins", 10, "light"))  # Poppins-Light para el botón

# style.configure("TLabel",
                # font=("Poppins", 10, "light"))  # Poppins-Light para la etiqueta

# style.configure("TCombobox",
                # font=("Poppins", 10, "light"))  # Poppins-Light para el combobox

title_label = tk.Label(root, text="SUBTITULADOR", fg="#bcf7f3", font=("Poppins", 24, "bold"),background="#00070d")
title_label.pack(pady=0)  # Añadir un espacio vertical
# Entrada y salida de archivos
frame_paths = tk.Frame(root)

frame_paths.pack(pady=5)
frame_paths.configure(bg="#0a1117")

tk.Label(frame_paths, text="Archivo de Entrada:",fg="#d3d4d5", bg="#0a1117").grid(row=0, column=0, padx=5, pady=2)
input_entry = tk.Entry(frame_paths, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=2)
browse_input_btn = tk.Button(frame_paths, text="Explorar", command=browse_input)
browse_input_btn.grid(row=0, column=2, padx=5, pady=2)

output_checkbox_var = tk.BooleanVar(value=True)
output_checkbox = tk.Checkbutton(frame_paths, text="Usar misma carpeta/nombre para salida", variable=output_checkbox_var)
output_checkbox.grid(row=1, column=1, columnspan=2, pady=2)

tk.Label(frame_paths, text="Archivo de Salida:",fg="#d3d4d5", bg="#0a1117").grid(row=2, column=0, padx=5, pady=2)
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
frame_settings.configure(bg="#080f15")
frame_settings.pack(fill="x", padx=10, pady=0)

# Primera columna de configuraciones básicas
frame_left = tk.Frame(frame_settings)
frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
frame_left.configure(bg="#080f15")
tk.Label(frame_left, text="Modelo:",fg="#d3d4d5", bg="#080f15").grid(row=0, column=0, padx=5, pady=5)
model_var = tk.StringVar(value="medium")
model_dropdown = ttk.Combobox(frame_left, textvariable=model_var, values=["tiny", "base", "small", "medium", "large"], state="readonly",style="TCombobox")
model_dropdown.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_left, text="Idioma:",fg="#d3d4d5", bg="#080f15").grid(row=1, column=0, padx=5, pady=5)
language_var = tk.StringVar(value="es")
language_dropdown = ttk.Combobox(frame_left, textvariable=language_var, values=["Auto", "en", "es", "fr", "de", "it"], state="readonly",style="TCombobox")
language_dropdown.grid(row=1, column=1, padx=5, pady=5)

timestamps_var = tk.BooleanVar(value=True)
timestamps_checkbox = tk.Checkbutton(frame_left, text="Habilitar Timestamps por palabra", variable=timestamps_var)
timestamps_checkbox.grid(row=2, column=0, columnspan=2, pady=5)

tk.Label(frame_left, text="Temperatura:",fg="#d3d4d5", bg="#080f15").grid(row=3, column=0, padx=5, pady=5)
temperature_var = tk.DoubleVar(value=0.5)
temperature_slider = tk.Scale(frame_left, variable=temperature_var, from_=0, to=1, resolution=0.1, orient="horizontal")
temperature_slider.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_left, text="Separación de Fragmentos:",fg="#d3d4d5", bg="#080f15").grid(row=4, column=0, padx=5, pady=5)
fragment_sep_entry = tk.Entry(frame_left, width=10)
fragment_sep_entry.grid(row=4, column=1, padx=5, pady=5)

# Segunda columna de configuraciones adicionales
frame_right = tk.Frame(frame_settings)
frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="ne")
frame_right.configure(bg="#080f15")
tk.Label(frame_right, text="Segment-level Timestamps:",fg="#d3d4d5", bg="#080f15").grid(row=0, column=0, padx=5, pady=5)
segment_level_var = tk.BooleanVar(value=True)
segment_level_checkbox = tk.Checkbutton(frame_right, text="Habilitar", variable=segment_level_var)
segment_level_checkbox.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_right, text="Word-level Timestamps:",fg="#d3d4d5", bg="#080f15").grid(row=1, column=0, padx=5, pady=5)
word_level_var = tk.BooleanVar(value=True)
word_level_checkbox = tk.Checkbutton(frame_right, text="Habilitar", variable=word_level_var)
word_level_checkbox.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_right, text="Duración Mínima (s):",fg="#d3d4d5", bg="#080f15").grid(row=2, column=0, padx=5, pady=5)
min_dur_var = tk.DoubleVar(value=0.2)
min_dur_entry = tk.Entry(frame_right, textvariable=min_dur_var, width=10)
min_dur_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_right, text="Tag Inicio/Fin:",fg="#d3d4d5", bg="#080f15").grid(row=3, column=0, padx=5, pady=5)
tag_entry = tk.Entry(frame_right, width=40)
tag_entry.insert(0, "('<font color=\"#00ff00\">', '</font>')")
tag_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_right, text="Formato VTT:",fg="#d3d4d5", bg="#080f15").grid(row=4, column=0, padx=5, pady=5)
vtt_var = tk.BooleanVar(value=False)
vtt_checkbox = tk.Checkbutton(frame_right, text="Habilitar", variable=vtt_var)
vtt_checkbox.grid(row=4, column=1, padx=5, pady=5)

tk.Label(frame_right, text="Texto Invertido:",fg="#d3d4d5", bg="#080f15").grid(row=5, column=0, padx=5, pady=0)
reverse_text_var = tk.BooleanVar(value=False)
reverse_text_checkbox = tk.Checkbutton(frame_right, text="Habilitar", variable=reverse_text_var)
reverse_text_checkbox.grid(row=5, column=1, padx=5, pady=0)

# Botón de convertir
#convert_btn = tk.Button(root, text="Convertir", command=convert_audio)
#convert_btn.pack(pady=10)
abrir_despues_var = tk.BooleanVar(value=False)

abrir_despues_checkbox = tk.Checkbutton(frame_paths, text="Abrir al generar", variable=abrir_despues_var)
abrir_despues_checkbox.grid(pady=3)
exportardespues_var = tk.BooleanVar(value=True)
exportardespues_checkbox = tk.Checkbutton(frame_paths, text="Exportar Transcripción", variable=exportardespues_var)
exportardespues_checkbox.grid(padx=4)


# Opciones avanzadas
frame_advanced = tk.LabelFrame(root, text="Opciones Avanzadas")
frame_advanced.configure(bg="#080f15")
frame_advanced.pack(fill="x", padx=10, pady=0)



# Tamaño de beam
tk.Label(frame_advanced, text="Tamaño de Beam:",fg="#d3d4d5", bg="grey10").grid(row=0, column=0, padx=5, pady=5)
beam_size_entry = tk.Entry(frame_advanced, width=10)
beam_size_entry.insert(0, "5")
beam_size_entry.grid(row=0, column=1, padx=5, pady=5)

# Tamaño de batch
tk.Label(frame_advanced, text="Tamaño de Batch:",fg="#d3d4d5", bg="grey10").grid(row=1, column=0, padx=5, pady=5)
batch_size_entry = tk.Entry(frame_advanced, width=10)
batch_size_entry.insert(0, "16")
batch_size_entry.grid(row=1, column=1, padx=5, pady=5)

# Tokens a suprimir
tk.Label(frame_advanced, text="Tokens a Suprimir:",fg="#d3d4d5", bg="grey10").grid(row=2, column=0, padx=5, pady=5)
suppress_tokens_entry = tk.Entry(frame_advanced, width=20)
suppress_tokens_entry.grid(row=2, column=1, padx=5, pady=5)

# Umbral de compresión
tk.Label(frame_advanced, text="Umbral de Compresión:",fg="#d3d4d5", bg="grey10").grid(row=3, column=0, padx=5, pady=5)
compression_ratio_entry = tk.Entry(frame_advanced, width=10)
#compression_ratio_entry.insert(0, "2.5")
compression_ratio_entry.grid(row=3, column=1, padx=5, pady=0)
# Etiqueta de estado
status_label = tk.Label(root, text="", fg="red")
status_label.pack(pady=5)
# Botón de convertir
convert_btn = tk.Button(root, text="Convertir", command=convert_audio)
convert_btn.pack(pady=10)


# Configuración de colores
root.configure(bg="#00070d")

# Frame Paths
frame_paths.configure(bg="#00070d")
tk.Label(frame_paths, text="Archivo de Entrada:",fg="#d3d4d5", bg="#00070d").config(bg="#00070d", fg="#d3d4d5")
input_entry.config(bg="#636d71", fg="white", insertbackground="grey1")
browse_input_btn.config(bg="#00070d", fg="white", activebackground="grey5", activeforeground="#bcf7f3")

output_checkbox.config(bg="#00070d", fg="#d3d4d5", selectcolor="#0a1117", activebackground="#00070d", activeforeground="white")
tk.Label(frame_paths, text="Archivo de Salida:",fg="#d3d4d5", bg="#00070d").config(bg="#00070d", fg="#d3d4d5")
output_entry.config(bg="#636d71", fg="white", insertbackground="grey1", disabledbackground="black")
browse_output_btn.config(bg="#00070d", fg="white", activebackground="grey5", activeforeground="#bcf7f3")

abrir_despues_checkbox.config(bg="#00070d", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="#bcf7f3")
exportardespues_checkbox.config(bg="#00070d", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="#bcf7f3")

# Frame Settings
frame_settings.config(bg="#080f15", fg="white")

# Primera columna en configuraciones básicas
frame_left.config(bg="#080f15")
tk.Label(frame_left, text="Modelo:", bg="#080f15").config(bg="#080f15", fg="white")
model_dropdown.config(background="#080f15", foreground="white")
tk.Label(frame_left, text="Idioma:",fg="#080f15", bg="#080f15").config(bg="#080f15", fg="white")
language_dropdown.config(background="#080f15", foreground="white")
timestamps_checkbox.config(bg="#080f15", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="#bcf7f3")
tk.Label(frame_left, text="Temperatura:",fg="#080f15", bg="#080f15").config(bg="#080f15", fg="white")
temperature_slider.config(bg="#080f15", fg="white", highlightbackground="#080f15", troughcolor="#0a1117")
tk.Label(frame_left, text="Separación de Fragmentos:",fg="#080f15", bg="#080f15").config(bg="#080f15", fg="white")
fragment_sep_entry.config(bg="#080f15", fg="white", )

# Segunda columna en configuraciones básicas
frame_right.config(bg="#080f15")
#tk.Label(frame_right, text="Segment-level Timestamps:").config(bg="#080f15", fg="white")
segment_level_checkbox.config(bg="#080f15", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="white")
tk.Label(frame_right, text="Word-level Timestamps:").config(bg="#080f15", fg="white")
word_level_checkbox.config(bg="#080f15", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="white")
tk.Label(frame_right, text="Duración Mínima (s):").config(bg="#080f15", fg="white")
min_dur_entry.config(bg="#0a1117", fg="white", insertbackground="yellow2")
tk.Label(frame_right, text="Tag Inicio/Fin:").config(bg="#080f15", fg="white")
tag_entry.config(bg="#0a1117", fg="white", insertbackground="yellow2")
tk.Label(frame_right, text="Formato VTT:").config(bg="#080f15", fg="white")
vtt_checkbox.config(bg="#080f15", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="white")
tk.Label(frame_right, text="Texto Invertido:").config(bg="#080f15", fg="white")
reverse_text_checkbox.config(bg="#080f15", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="white")

# Frame Advanced
frame_advanced.config(bg="#080f15", fg="white")
tk.Label(frame_advanced, text="Tamaño de Beam:").config(bg="#080f15", fg="white")
beam_size_entry.config(bg="#0a1117", fg="white", insertbackground="white")
tk.Label(frame_advanced, text="Tamaño de Batch:").config(bg="#080f15", fg="white")
batch_size_entry.config(bg="#0a1117", fg="white", insertbackground="white")
tk.Label(frame_advanced, text="Tokens a Suprimir:").config(bg="#080f15", fg="white")
suppress_tokens_entry.config(bg="#0a1117", fg="white", insertbackground="white")
tk.Label(frame_advanced, text="Umbral de Compresión:").config(bg="#080f15", fg="white")
compression_ratio_entry.config(bg="#0a1117", fg="white", insertbackground="yellow2")

# Botón Convertir
convert_btn.config(bg="#3b4146", fg="white", activebackground="green1", activeforeground="yellow2")

# Etiqueta de estado
status_label.config(bg="#3b4146", fg="red")


if not os.path.exists(CONFIG_FILE):
    default_config = {
        "input_path": "",
        "output_path": "",
        "model_name": "medium",
        "language": "Auto",
        "word_timestamps": False,
        "temperature": 0.5,
        "max_initial_timestamp": 0.0,
        "beam_size": 5,
        "batch_size": 16,
        "suppress_tokens": "",
        "compression_ratio_threshold": 2.5,
        "segment_level": True,
        "word_level": True,
        "tag": "('<font color=\"#00ff00\">', '</font>')",
        "vtt": False,
        "reverse_text": False,
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(default_config, file, indent=4)

def apply_config():
    config = load_config()

    # Rellenar entradas con valores cargados
    input_entry.insert(0, config.get("input_path", ""))
    output_entry.insert(0, config.get("output_path", ""))
    model_var.set(config.get("model_name", "medium"))
    language_var.set(config.get("language", "Auto"))
    timestamps_var.set(config["word_timestamps"].get())
    temperature_var.set(config["temperature"].get())
    fragment_sep_entry.insert(0, str(config.get("max_initial_timestamp", "")))
    beam_size_entry.insert(0, str(config.get("beam_size", "5")))
    batch_size_entry.insert(0, str(config.get("batch_size", "16")))
    suppress_tokens_entry.insert(0, config.get("suppress_tokens", ""))
    compression_ratio_entry.insert(0, str(config.get("compression_ratio_threshold", "2.5")))
    segment_level_var.set(config["segment_level"].get())
    word_level_var.set(config["word_level"].get())
    tag_entry.insert(0, config.get("tag", "<font color=\"#00ff00\">, </font>"))
    vtt_var.set(config["vtt"].get())
    reverse_text_var.set(config["reverse_text"].get())

apply_config()

root.mainloop()
