import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
import os
import stable_whisper
import json
import sys
import threading

CONFIG_FILE = "config.json"
# Verificar si el archivo existe

script_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta completa a la carpeta 'temps'
temps_dir = os.path.join(script_dir, 'temp')
# Contenido predeterminado para el archivo JSON
default_config = {
    "verbose": False,
    "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
    "compression_ratio_threshold": 2.4,
    "logprob_threshold": -1,
    "no_speech_threshold": 0.6,
    "condition_on_previous_text": True,
    "initial_prompt": None,
    "word_timestamps": True,
    "regroup_var": True,
    "suppress_silence": True,
    "suppress_word_ts": True,
    "use_word_position": True,
    "q_levels": 20,
    "k_size": 5,
    "denoiser": None,
    "denoiser_options": None,
    "vad": False,
    "vad_threshold": 0.35,
    "min_word_dur": None,
    "min_silence_dur": None,
    "nonspeech_error": 0.1,
    "only_voice_freq": False,
    "prepend_punctuations": False,
    "append_punctuations": False,
    "stream": None,
    "mel_first": None,
    "split_callback": None,
    "suppress_ts_tokens_": False,
    "gap_padding": " ...",
    "only_ffmpeg": False,
    "max_instant_words": 0.5,
    "avg_prob_threshold": None,
    "nonspeech_skip": None,
    "progress_callback": None,
    "ignore_compatibility": False,
    "extra_models": None,
    "dynamic_heads": None,
    "model": "base",
    "device": "cpu",
    "temps_dir": temps_dir  ,
    "audio": None,
    "model_eng": False,
    "timestampmode": 'Linea a linea'
}
if not os.path.exists(CONFIG_FILE):
    # Si no existe, crear el archivo con la configuración predeterminada
    with open(CONFIG_FILE, "w") as file:
        json.dump(default_config, file, indent=4)
    print(f"El archivo {CONFIG_FILE} ha sido creado con la configuración predeterminada.")
else:
    # Si existe, cargar la configuración
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)
    print(f"El archivo {CONFIG_FILE} ha sido cargado.")


overridesrt= False

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
        model_var = tk.StringVar(value=data.get("model"))
        device_var = tk.StringVar(value=data.get("device"))
        temps_dir = data.get("temps_dir")
        input_entry.delete(0, tk.END)
        if data.get("audio") != None:
            input_entry.insert(0, data.get("audio"))
        verbose_var = data.get("verbose")
        temp_entry.delete(0, tk.END)
        temp_entry.insert(0, data.get("temperature"))
        no_speech_threshold_var = tk.DoubleVar(value= data.get("no_speech_threshold"))
        initial_prompt_var = data.get("initial_prompt")
        if initial_prompt_var != None:
            initial_prompt_var_entry.insert(0, initial_prompt_var)
        model_eng.set(data.get("model_eng"))
        timestampmode.set(data.get("timestampmode"))
    except FileNotFoundError:
        print("Archivo de configuración no encontrado. Se usará configuración predeterminada.")
        return {}

def cargarmodelo():
    status_model.config(text="Cargando modelo...", fg="blue")
    global modeloactual

    try:
        model_name = model_var.get() 
        if model_eng.get() == True:
            if model_name != "Large":
                model_name = model_name+".en"
        modeloactual = stable_whisper.load_model(
            name=model_var.get(),                    
            device=device_var.get(),                
            download_root=temps_dir,  
            in_memory=in_memory_var,          
            cpu_preload=cpu_preload_var,      
            dq=dq_var                         
            )          
    except Exception as e:      
        status_model.config(text=f"Error!: {str(e)}", fg="red")
    else:
        status_model.config(text=f"Finalizado! Guardando config...")
        modelo_hint.configure(text="Cargado: "+device_var.get()+ " " + model_name)
        try:
            with open(CONFIG_FILE, "r") as file:
                 config = json.load(file)

            # # Actualizar las variables en el archivo de configuración
            config["model"] = model_var.get()
            config["device"] = device_var.get()
            # config["download_root"] = download_root_var
            # config["in_memory"] = in_memory_var
            # config["cpu_preload"] = cpu_preload_var
            # config["dq"] = dq_var
            

            save_config(config)
        except Exception as e:
            status_model.config(text=f"Error!: {str(e)}", fg="yellow")
        else:
            status_model.config(text=f"Modelo Cargado", fg="green")
def transcribir_audio():
    status_model.config(text=f"transcribiendo...", fg="blue")
    """
    Llama a la función `transcribe()` con todos los parámetros definidos previamente como variables.
    """
    try:
        modeloactual
    except NameError:
    # Si 'modeloactual' no está definida, ejecutar 'cargarmodelo()'
        cargarmodelo()
    if input_entry.get() == "":
        browse_input()
        
    if temp_chk.get():
        temperature_var = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
    else:
        try:
        # Intentar convertir el valor ingresado en un número
            user_input = float(temp_entry.get())
        # Usar un valor único como lista o tupla de un elemento
            temperature_var = (user_input,)
        except ValueError:
        # Si el valor ingresado no es válido
            status_model.config(text="Error: El valor ingresado no es válido.", fg="red")
            return
    global t_actual
    
    try: 
        t_actual = modeloactual.transcribe(
            audio=input_entry.get(),
            verbose=verbose_var,
            temperature=temperature_var,
            no_speech_threshold=no_speech_threshold_var.get(),
            initial_prompt= initial_prompt_var_entry.get()
        )
    except Exception as e:
        status_model.config(text=f"Error!: {str(e)}", fg="red")
    else:
        status_model.config(text=f"Finalizado! Guardando config...")
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0",  str(t_actual.text)) 
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)

            # Actualizar las variables en el archivo de configuración
            # config["model"] = model_var
            config["audio"] = input_entry
            config["verbose"] = verbose_var
            config["temperature"] = temperature_var
            # config["compression_ratio_threshold"] = compression_ratio_threshold_var
            # config["logprob_threshold"] = logprob_threshold_var
            config["no_speech_threshold"] = no_speech_threshold_var.get()
            # config["condition_on_previous_text"] = condition_on_previous_text_var
            config["initial_prompt"] = initial_prompt_var_entry.get()
            # config["word_timestamps"] = word_timestamps_var
            # config["regroup"] = regroup_var
            # config["suppress_silence"] = suppress_silence_var
            # config["suppress_word_ts"] = suppress_word_ts_var
            # config["use_word_position"] = use_word_position_var
            # config["q_levels"] = q_levels_var
            # config["k_size"] = k_size_var
            # config["denoiser"] = denoiser_var
            # config["denoiser_options"] = denoiser_options_var
            # config["vad"] = vad_var
            # config["vad_threshold"] = vad_threshold_var
            # config["min_word_dur"] = min_word_dur_var
            # config["min_silence_dur"] = min_silence_dur_var
            # config["nonspeech_error"] = nonspeech_error_var
            # config["only_voice_freq"] = only_voice_freq_var
            # config["prepend_punctuations"] = prepend_punctuations_var
            # config["append_punctuations"] = append_punctuations_var
            # config["stream"] = stream_var
            # config["mel_first"] = mel_first_var
            # config["split_callback"] = split_callback_var
            # config["suppress_ts_tokens"] = suppress_ts_tokens_var
            # config["gap_padding"] = gap_padding_var
            # config["only_ffmpeg"] = only_ffmpeg_var
            # config["max_instant_words"] = max_instant_words_var
            # config["avg_prob_threshold"] = avg_prob_threshold_var
            # config["nonspeech_skip"] = nonspeech_skip_var
            # config["progress_callback"] = progress_callback_var
            # config["ignore_compatibility"] = ignore_compatibility_var
            # config["extra_models"] = extra_models_var
            # config["dynamic_heads"] = dynamic_heads_var

            # Guardar el archivo JSON con las actualizaciones
            save_config(config)
        except Exception as e:
            status_model.config(text=f"Error!: {str(e)}", fg="yellow")
        else:
            status_model.config(text=f"Finalizado!", fg="green")

    # Puedes aquí agregar un `print` para mostrar el estado o realizar otras acciones si lo necesitas
def cargarmodeloproceso():
    # Usar un hilo para que la interfaz gráfica no se bloquee
    threading.Thread(target=cargarmodelo).start()
    
def audioproceso():
    # Usar un hilo para que la interfaz gráfica no se bloquee
    threading.Thread(target=transcribir_audio).start()    
def pronto():
    # Crear una nueva ventana emergente
    popup = tk.Toplevel()
    popup.title("Aviso")
    popup.geometry("200x100")
    popup.resizable(False, False)
    
    # Etiqueta con el mensaje
    label = tk.Label(popup, text="Próximamente", font=("Arial", 12))
    label.pack(pady=10)
    
    # Botón "Aceptar" para cerrar la ventana
    aceptar_btn = tk.Button(popup, text="Aceptar", command=popup.destroy)
    aceptar_btn.pack(pady=10)

    # Mantener la ventana emergente centrada
    popup.transient()  # La ventana permanece sobre el padre
    popup.grab_set()   # Bloquea interacción con otras ventanas hasta que se cierre
    popup.wait_window()  # Espera hasta que la ventana sea cerrada

    
if True == True:
    verbose_var = False
    temperature_var = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
    compression_ratio_threshold_var = 2.4
    logprob_threshold_var = -1
    no_speech_threshold_var = 0.6
    condition_on_previous_text_var = True
    initial_prompt_var = None
    word_timestamps_var = True
    regroup_var = True 
    suppress_silence_var = True
    suppress_word_ts_var = True
    use_word_position_var = True
    q_levels_var = 20
    k_size_var = 5
    denoiser_var = None
    denoiser_options_var = None
    vad_var = False
    vad_threshold_var = 0.35
    min_word_dur_var = None
    min_silence_dur_var = None
    nonspeech_error_var = 0.1
    only_voice_freq_var = False
    prepend_punctuations_var = False
    append_punctuations_var = False
    stream_var = None
    mel_first_var = None
    split_callback_var = None
    suppress_ts_tokens_var = False
    gap_padding_var = ' ...'
    only_ffmpeg_var = False
    max_instant_words_var = 0.5
    avg_prob_threshold_var = None
    nonspeech_skip_var = None
    progress_callback_var = None
    ignore_compatibility_var = False
    extra_models_var = None
    dynamic_heads_var = None

def modelo_defactos():
    global model_var, device_var, download_root_var, in_memory_var, cpu_preload_var, dq_var, engine_var
    model_var.set('base')
    device_var.set('cpu')
    temps_dir = os.path.join(script_dir, 'temp')
    if not os.path.exists(temps_dir):
        os.makedirs(temps_dir)
    download_root_var = temps_dir
    in_memory_var = False
    cpu_preload_var = True
    dq_var = False
    engine_var = None
    model_eng.set(False)

def guardar_srt():
    output_path = output_entry.get() if (output_checkbox_var.get() ==  False) else f"{input_entry.get().rsplit('.', 1)[0]}.srt"
    status_model.config(text="Guardando SRT", fg="blue")
    try:
        #tag_value = tag_entry.get()

           # Asegúrate de evaluar la cadena como una tupla
        #tag_tuple = eval(tag_value)  # Evalúa la cadena y la convierte en tupla
        
        if not overridesrt:
            if timestampmode.get() == "Linea a linea":
                segment_level_var = True
                word_level_var = False
            elif timestampmode.get() == "Palabra a palabra":
                segment_level_var = False
                word_level_var = True
            elif timestampmode.get() == "Linea con Highlight":
                segment_level_var = True
                word_level_var = True
            else:
                status_model.config(text="ERROR CONFIG", fg="red")
                
        t_actual.to_srt_vtt(
            output_path,
            segment_level=segment_level_var ,
            word_level=word_level_var,
            #min_dur=min_dur_var.get(),
            #tag=tag_tuple,
            #vtt=vtt_var.get(),
            #reverse_text=reverse_text_var.get(),
            )
        
        
        status_model.config(text=".srt exitoso", fg="green")
        if abrir_despues_var.get():
            os.startfile(output_path)  # En Windows
    except Exception as e:
        status_model.config(text=f"Hubo un problema: {str(e)}", fg="red")
    else:
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)

            # Actualizar las variables en el archivo de configuración
            # config["model"] = model_var
            config["output_path"] = output_path
            config["segment_level"] = segment_level_var.get()
            config["word_level"] = word_level_var.get() 
            config["timestampmode"] =  timestampmode.get()
            save_config(config)
        except Exception as e:
            status_model.config(text=f"Error!: {str(e)}", fg="yellow")
        else:
            status_model.config(text=f"Finalizado!", fg="green")
def guardar_txt():
     
    output_path = f"{output_entry.get().rsplit('.', 1)[0]}.txt" if (output_checkbox_var.get() ==  False) else f"{input_entry.get().rsplit('.', 1)[0]}.txt"
    status_model.config(text="Guardando TXT", fg="blue")
    try:
       
        t_actual.to_txt(output_path)

        status_model.config(text=".srt exitoso", fg="green")
        if abrir_despues_var.get():
            os.startfile(output_path)  # En Windows
    except Exception as e:
        status_model.config(text=f"Hubo un problema: {str(e)}", fg="red")
    else:
        status_model.config(text=f"TXT exportado!", fg="green")
   
    
    
def browse_input():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos de audio y video", "*.mp3 *.wav *.m4a *.flac *.m4a *.mp4 *.avi *.mov *.aac *.ogg *.webm *.aiff *.amr *.mka *.mp4 *.3gp *.wma")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def browse_output():
    file_path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT Files", "*.srt")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)    
    
    
 
    
class RedirectOutput:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Scroll automático

    def flush(self):
        pass  # Necesario para ser compatible con stdout/err
  
  
  
  
  
# ventana principal
root = tk.Tk()
root.title("Transcriptor de Audio")
root.geometry("710x820")  # Ancho ajustado para acomodar dos columnas
root.resizable(False,False)
root.configure(bg="#00070d")
try:
        # Cargar la fuente desde el archivo Poppins-Regular.ttf
        poppins_fuente = font.Font(family="Poppins", size=8)
        # Si la fuente no está instalada, puedes intentar cargarla directamente desde un archivo
        poppins_fuente.config(file="Poppins-Medium.ttf")
except Exception as e:
        print(f"Error al cargar la fuente: {e}")
        # Si no se puede cargar la fuente, usa una fuente predeterminada
        poppins_fuente = font.Font(family="Helvetica", size=9)

root.option_add("*Font", poppins_fuente) 
# Set popdown listbox styling via the option database
root.option_add('*TCombobox*Listbox.background', '#00070d')  # Background of the listbox
root.option_add('*TCombobox*Listbox.foreground', 'black')     # Text color in the listbox
root.option_add('*TCombobox*Listbox.selectBackground', '#d3d4d5')  # Selection background color
root.option_add('*TCombobox*Listbox.selectForeground', '#00070d')    # Selection text color    
style = ttk.Style()
style.configure("TCombobox",
                arrowcolor="#bcf7f3",         # Color of the dropdown arrow
                arrowsize=10,               # Size of the dropdown arrow
                background="black",         # Background of the combobox entry
                foreground="black",        # Text color inside the combobox
                fieldbackground="black",    # Background color of the entry field
                insertcolor="red",       # Cursor color
                insertwidth=5,              # Width of the cursor
                selectbackground="darkgrey", # Selection background color
                selectforeground="#bcf7f3")   # Selection text color
                
style.configure("TScale",
                background="#080f15",          # Fondo general
                troughcolor="darkgrey",      # Color del canal (trough)
                sliderrelief="flat",         # Apariencia del slider
                sliderthickness=5,          # Grosor del slider
                sliderlength=30,             # Longitud del slider
                sliderbackground="#bcf7f3")  # Color del slider

# Colores para los estados del Combobox
style.map("TCombobox",
                   background=[('disabled', 'yellow2'),  # Fondo cuando está deshabilitado
                               ('active', 'yellow3')],    # Fondo cuando está activo (ratón encima)
                   foreground=[('disabled', 'green1')],
                    relief=[('pressed', '!disabled', 'sunken')])  # Color del texto cuando está deshabilitado  
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
output_checkbox.config(bg="#080f15", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="#bcf7f3")
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
frame_modelo = tk.LabelFrame(root, text="Config de modelo IA", fg="#bcf7f3")
frame_modelo.configure(bg="#080f15")
frame_modelo.pack(fill="x", padx=10, pady=0)

# Configuración de la estructura de columnas
frame_modelo.grid_columnconfigure(0, weight=0, uniform="equal")  # Primera columna flexible
frame_modelo.grid_columnconfigure(1, weight=0)  # Segunda columna flexible
frame_modelo.grid_columnconfigure(2, weight=0)  # Tercera columna fija
#  Primera columna de configuraciones básicas
frame_left = tk.Frame(frame_modelo)
frame_left.grid(row=0, column=0, padx=5, pady=10, sticky="w")
frame_left.configure(bg="#080f15")

frame_mid = tk.Frame(frame_modelo)
frame_mid.grid(row=0, column=2, padx=0, pady=0, sticky="nw")
frame_mid.configure(bg="#080f15")

frame_right = tk.Frame(frame_modelo)
frame_right.grid(row=0, column=1, padx=0, pady=0, sticky="nw")
frame_right.configure(bg="#080f15")

tk.Label(frame_left, text="Modelo:",fg="#d3d4d5", bg="#080f15").grid(row=0, column=0, padx=5, pady=5)
model_var = tk.StringVar(value="medium")
model_dropdown = ttk.Combobox(frame_left, textvariable=model_var, values=["tiny", "base", "small", "medium", "large"], state="readonly",style="TCombobox")
model_dropdown.config(background="red", foreground="black")
model_dropdown.grid(row=0, column=1, padx=0, pady=0)

model_eng = tk.BooleanVar(value=True)
model_engchk = tk.Checkbutton(frame_left, text="Forzar solo inglés", variable=model_eng)
model_engchk.config(bg="#080f15", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="#bcf7f3")
model_engchk.grid(row=1, column=1, columnspan=1, pady=0)      

tk.Label(frame_left, text="Procesamiento:",fg="#d3d4d5", bg="#080f15").grid(row=3, column=0, padx=5, pady=5)          
device_var = tk.StringVar(value='cuda')
device_chk = ttk.Combobox(frame_left, textvariable=device_var, values=['cpu', 'cuda'], state="readonly",style="TCombobox")
device_chk.grid(row=3, column=1, padx=0, pady=0) 


# Segunda columna de configuraciones adicionales
#modelo_hint2 = tk.Label(frame_mid, text=" ",fg="darkgray", bg="#080f15")
#modelo_hint2.grid(row=1, column=8, padx=5, pady=0)
modelo_hint = tk.Label(frame_mid, text="Sin modelo cargado",fg="darkgray", bg="#080f15")
modelo_hint.grid(row=2, column=8, padx=5, pady=10)

tk.Label(frame_left, text="      ",fg="darkgray", bg="#080f15").grid(row=0, column=7, padx=0, pady=5)

cargar_btn = tk.Button(frame_right, text="Avanzados...", command=pronto, width=22)
cargar_btn.pack(pady=16)
cargar_btn.config(bg="#3b4146", fg="white", activebackground="grey12", activeforeground="white")
convert_btn2 = tk.Button(frame_right, text="Restaurar por defecto", command=modelo_defactos, width=22)
convert_btn2.pack(padx=10,pady=2)
convert_btn2.config(bg="#3b4146", fg="white", activebackground="grey12", activeforeground="white")    



status_model = tk.Label(root, text="Preparado.",fg="darkgray", bg="black")    
status_model.pack(padx=0, pady=15)



btn3 = tk.Button(frame_mid, text="Cargar\nmodelo", command=cargarmodeloproceso, width=20)
btn3.grid(row=3, column=8, padx=5, pady=4)
btn3.config(bg="#3b4146", fg="white", activebackground="grey12", activeforeground="white")  
#####################################
frame_texto = tk.LabelFrame(root, text="Config Subtitulado", fg="#bcf7f3")
frame_texto.configure(bg="#080f15")
frame_texto.pack(fill="x", padx=10, pady=0)

frame_tleft = tk.Frame(frame_texto)
frame_tleft.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
frame_tleft.configure(bg="#080f15")

#frame_tmid = tk.Frame(frame_texto)
#frame_tmid.grid(row=0, column=1, padx=0, pady=0, sticky="n")
#frame_tmid.configure(bg="#080f15")

frame_tright = tk.Frame(frame_texto)
frame_tright.grid(row=0, column=2, padx=00, pady=0, sticky="nw")
frame_tright.configure(bg="#080f15")

tk.Label(frame_tleft, text="Añadir palabras:",fg="#d3d4d5", bg="#080f15").grid(row=0, column=0, padx=5, pady=5)
initial_prompt_var_entry = tk.Entry(frame_tleft, width=25)
initial_prompt_var_entry.delete(0, tk.END)
initial_prompt_var_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_tleft, text="Dinamica:",fg="#d3d4d5", bg="#080f15").grid(row=1, column=0, padx=5, pady=5)          
timestampmode = tk.StringVar(value='Linea a linea')
device_chk = ttk.Combobox(frame_tleft, textvariable=timestampmode, values=['Linea a linea', 'Palabra a palabra', 'Linea con Highlight'], state="readonly",style="TCombobox")
device_chk.grid(row=1, column=1, padx=5, pady=0) 


tk.Label(frame_tright, text="Temperatura:",fg="#d3d4d5", bg="#080f15").grid(row=0, column=0, padx=5, pady=5)
temp_entry = tk.Entry(frame_tright, width=25)
temp_entry.insert(0, "(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)")
temp_entry.grid(row=0, column=1, padx=5, pady=5)

def toggle_temp():
    state = tk.NORMAL if not temp_chk.get() else tk.DISABLED
    temp_entry.config(state=state)
  
    

temp_chk = tk.BooleanVar(value=True)
temp_chkb = tk.Checkbutton(frame_tright, text="AUTO", variable=temp_chk, command=toggle_temp, )
temp_chkb.config(bg="#080f15", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="#bcf7f3")
temp_chkb.grid(row=0, column=2, columnspan=1, pady=0)      

label = ttk.Label(frame_tright, text="Umbral No Speech:")
label.grid(row=2, column=0)
label.config(foreground="#d3d4d5", background="#080f15")
no_speech_threshold_var = tk.DoubleVar(value=0.6)  # Valor inicial
def actualizar_nst(*args):
    valor_actual_label.config(text=f"Valor actual: {no_speech_threshold_var.get():.2f}")
slider = ttk.Scale(
    frame_tright, 
    from_=0.0,  # Valor mínimo
    to=1.0,     # Valor máximo
    orient="horizontal", 
    variable=no_speech_threshold_var, 
    command=actualizar_nst,  # Actualizar cuando se mueva el slider,
    #foreground="#d3d4d5", background="#080f15"
    style="TScale"
)
slider.grid(row=2, column=1)

valor_actual_label = ttk.Label(frame_tright, text="Valor actual: 0.5",foreground="#d3d4d5", background="#080f15")
valor_actual_label.grid(row=4, column= 1)
no_speech_threshold_var.trace_add("write", actualizar_nst)
##########################################################################


botonera = tk.Frame(root)
botonera.pack( padx=20, pady=8)

# Cambiar el color de fondo del ttk.Frame a negro
botonera.configure(background="black")  # Aplicar directamente el color de fondo


btn4 = tk.Button(botonera, text="Procesar\narchivo", command=audioproceso, width=15)
btn4.pack(side="left",padx=12, pady=4)
btn4.config(bg="green3", fg="white", activebackground="springgreen2", activeforeground="black")  
btnsrt = tk.Button(botonera, text="Guardar\n.srt", command=guardar_srt, width=15)
btnsrt.pack(side="left",padx=2, pady=4)
btnsrt.config(bg="#3b4146", fg="white", activebackground="grey12", activeforeground="white") 
btntxt = tk.Button(botonera, text="Guardar\ntexto", command=guardar_txt, width=15)
btntxt.pack(side="left",padx=2, pady=4)
btntxt.config(bg="#3b4146", fg="white", activebackground="grey12", activeforeground="white") 

abrir_despues_var = tk.BooleanVar(value=True)
abrir_despues = tk.Checkbutton(botonera, text="Abrir al crear", variable=abrir_despues_var, command=toggle_temp, )
abrir_despues.config(bg="#00070d", fg="white", selectcolor="#0a1117", activebackground="#00070d", activeforeground="#bcf7f3")
abrir_despues.pack(pady=0)  

###############################################################################################################
frame_vista = tk.LabelFrame(root, text="Preview", fg="#bcf7f3")
frame_vista.configure(bg="#080f15")
frame_vista.pack(fill="x", padx=10, pady=0)

text_widget = tk.Text(frame_vista, wrap="word")  # wrap="word" ajusta líneas por palabras
text_widget.pack(side="left", fill="both", expand=True,padx=2, pady=10)

# Crear una barra de desplazamiento vertical
scrollbar = ttk.Scrollbar(frame_vista, orient="vertical", command=text_widget.yview)
scrollbar.pack(side="right", fill="y")

# Configurar el widget Text para que use la barra de desplazamiento
text_widget.configure(yscrollcommand=scrollbar.set, bg="#080f15", fg="white")

# Insertar texto largo en el widget Text
texto_largo = ""
text_widget.insert("1.0", texto_largo)  # Insertar texto en la posición inicial


sys.stdout = RedirectOutput(text_widget)
sys.stderr = RedirectOutput(text_widget)

modelo_defactos()

toggle_temp()  
load_config()


#####################################
### HINTS ####
#####################################

#Transcribe
model_var_hint = "Instancia del modelo Whisper, utilizada para procesar y transcribir el audio."
audio_var_hint = "Archivo de audio a transcribir, que puede ser un archivo local, una URL, un array de numpy, un tensor de PyTorch o bytes."
verbose_var_hint = "Controla qué se muestra en la consola durante la transcripción. True muestra todo, False solo la barra de progreso, y None no muestra nada."
temperature_var_hint = "Define valores para la temperatura de muestreo, afectando la diversidad en los resultados. Una lista permite ajustes progresivos."
compression_ratio_threshold_var_hint = "Umbral que marca un segmento como fallido si su relación de compresión gzip excede este valor."
logprob_threshold_var_hint = "Define un umbral de probabilidad logarítmica promedio bajo el cual un segmento se considera fallido."
no_speech_threshold_var_hint = "Probabilidad mínima para clasificar un segmento como silencio."
condition_on_previous_text_var_hint = "Decide si el texto de la ventana anterior se usa como contexto para la próxima transcripción."
initial_prompt_var_hint = "Proporciona un contexto inicial para mejorar la precisión en nombres propios, vocabulario personalizado, etc."
word_timestamps_var_hint = "Activa o desactiva la generación de marcas de tiempo a nivel de palabras."
regroup_var_hint = "Controla el algoritmo de reagrupar segmentos basado en puntuación y silencios."
suppress_silence_var_hint = "Ajusta las marcas de tiempo en función de los silencios detectados."
suppress_word_ts_var_hint = "Ajusta las marcas de tiempo a nivel de palabra para evitar saltos durante los silencios."
use_word_position_var_hint = "Decide cómo ajustar las marcas de tiempo según la posición de las palabras."
q_levels_var_hint = "Niveles de cuantización para marcar silencios."
k_size_var_hint = "Tamaño del kernel para el promedio móvil usado al generar la máscara de supresión de tiempo."
denoiser_var_hint = "Define el denoiser a usar para la limpieza previa del audio."
denoiser_options_var_hint = "Opciones adicionales para configurar el denoiser."
vad_var_hint = "Activa el uso de Silero VAD para detectar voz y ajustar silencios."
vad_threshold_var_hint = "Umbral para el detector de voz Silero VAD."
min_word_dur_var_hint = "Duración mínima permitida para una palabra tras aplicar supresión de silencios."
min_silence_dur_var_hint = "Duración mínima de silencio permitida."
nonspeech_error_var_hint = "Error relativo permitido en las secciones de no habla."
only_voice_freq_var_hint = "Limita la detección al rango de frecuencia de la voz humana (200-5000 Hz)."
prepend_punctuations_var_hint = "Puntuación que se añade al inicio de la siguiente palabra."
append_punctuations_var_hint = "Puntuación que se añade al final de la palabra anterior."
stream_var_hint = "Define si el audio se carga en fragmentos."
mel_first_var_hint = "Procesa todo el audio en un espectrograma log-Mel antes de transcribir."
split_callback_var_hint = "Callback personalizado para agrupar tokens y palabras."
suppress_ts_tokens_var_hint = "Suprime marcas de tiempo generadas en silencios durante la inferencia."
gap_padding_var_hint = "Texto de relleno para alinear marcas de tiempo."
only_ffmpeg_var_hint = "Usa solo FFmpeg para procesar URLs."
max_instant_words_var_hint = "Porcentaje máximo de palabras instantáneas permitido antes de descartar un segmento."
avg_prob_threshold_var_hint = "Umbral de probabilidad promedio para descartar segmentos con baja confianza."
nonspeech_skip_var_hint = "Duración mínima de no habla para saltar esas secciones."
progress_callback_var_hint = "Callback para actualizar el progreso de la transcripción."
ignore_compatibility_var_hint = "Ignora advertencias de incompatibilidad con la versión de Whisper."
extra_models_var_hint = "Lista de modelos adicionales para extraer marcas de tiempo a nivel de palabra."
dynamic_heads_var_hint = "Optimiza los heads de atención cruzada en tiempo de ejecución."
decode_options_var_hint = "Argumentos adicionales para construir opciones de decodificación."
##################
####VTT
segment_level_hint = "Permite incluir marcas de tiempo para segmentos completos."
word_level_hint = "Agrega marcas de tiempo a nivel de palabras individuales."
min_dur_hint = "Define la duración mínima que deben tener las palabras o segmentos; segmentos más cortos serán combinados con adyacentes."
tag_hint = "Personaliza etiquetas HTML para destacar palabras en el archivo."
vtt_hint = "Determina si el archivo generado será VTT o no (por defecto depende de la extensión)."
strip_hint = "Elimina espacios en blanco innecesarios de cada segmento."
reverse_text_hint = "Modifica el orden de las palabras en el segmento o ajusta puntuaciones de inicio y final."


root.mainloop()