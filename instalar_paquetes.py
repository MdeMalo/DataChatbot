import subprocess
import os
import tkinter as tk
from tkinter import scrolledtext

apt_ups = False

def instalar_paquete(paquete):
    global apt_ups
    try:
        __import__(paquete)
    except ImportError:
        print(f"El paquete '{paquete}' no está instalado. Instalando...")
        if not apt_ups:
            try:
                subprocess.check_call(["sudo", "apt", "update"])
                subprocess.check_call(["sudo", "apt", "upgrade", "-y"])
                apt_ups = True
            except subprocess.CalledProcessError as e:
                print(f"Error al actualizar y mejorar los paquetes del sistema: {e}")
        try:
            subprocess.check_call(["sudo", "apt", "install", f"python3-{paquete}", "-y"])
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar el paquete {paquete}: {e}")
            
def instalar_paquete_sistema(paquete):
    """
    Comprueba e instala un paquete de sistema usando dpkg.
    """
    try:
        # dpkg -s devuelve 0 si el paquete está instalado
        resultado = subprocess.run(["dpkg", "-s", paquete], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if resultado.returncode != 0:
            print(f"El paquete de sistema '{paquete}' no está instalado. Instalando...")
            subprocess.check_call(["sudo", "apt", "update"])
            subprocess.check_call(["sudo", "apt", "install", paquete, "-y"])
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar el paquete de sistema '{paquete}': {e}")

def comprobar_e_instalar_paquetes():
    paquetes = [
        "matplotlib",
        "requests",
        "tkinter"
    ]

    for paquete in paquetes:
        instalar_paquete(paquete)
        
    paquetes_sistema = [
        "lm-sensors",
        "dmidecode",
        "lshw",
        "lsb-release"
    ]
    for paquete in paquetes_sistema:
        instalar_paquete_sistema(paquete)

def mostrar_bibliotecas():
    archivo = './datos/requirements.txt'
    ventana_historial = tk.Tk()  # Crea una ventana secundaria
    ventana_historial.title("Historial del Chat")
    ventana_historial.geometry("800x600")  # Establece un tamaño mayor
    ventana_historial.resizable(True, True)  # Permite redimensionar la ventana

    texto_historial = scrolledtext.ScrolledText(ventana_historial, width=100, height=20, wrap=tk.WORD)
    texto_historial.pack(expand=True, fill='both')

    try:
        with open(archivo, 'r', encoding="utf-8") as file:
            contenido = file.read()
        if not contenido.strip():
            contenido = "El archivo está vacío."
        texto_historial.insert(tk.INSERT, contenido)
        texto_historial.config(state=tk.DISABLED)
    except FileNotFoundError:
        texto_historial.insert(tk.INSERT, "El archivo 'requirements.txt' no se encontró.")
        texto_historial.config(state=tk.DISABLED)
        
def comprobar_Archivos():
    if not os.path.exists("datos"):
        os.makedirs("datos")
    
    if not os.path.exists("./datos/temp.txt"):
        with open("./datos/temp.txt", 'w', encoding='utf-8') as file:
            pass

    if not os.path.exists("./datos/datos_temperaturas.csv"):
        with open("./datos/datos_temperaturas.csv", 'w', encoding='utf-8') as file:
            pass
        
    if not os.path.exists("./datos/datos_bios.txt"):
        with open("./datos/datos_bios.txt", 'w', encoding='utf-8') as file:
            pass
        
    if not os.path.exists("./datos/datos_lshw.txt"):
        with open("./datos/datos_lshw.txt", 'w', encoding='utf-8') as file:
            pass
        
    if not os.path.exists("./datos/datos_OS.txt"):
        with open("./datos/datos_OS.txt", 'w', encoding='utf-8') as file:
            pass
        
    if not os.path.exists("./datos/historial_Chat.txt"):
        with open("./datos/historial_Chat.txt", 'w', encoding='utf-8') as file:
            pass
        
    if not os.path.exists("./datos/requirements.txt"):
        with open("./datos/requirements.txt", 'w', encoding='utf-8') as file:
            file.write("Las bibliotecas necesarias son: \ncsv\ntime\nshutil\nos\nre\nrandom\nsubprocess\n" \
                "matplotlib\nrequests\nsys\ntkinter\nPueden ser inctaladas con:\n   pip install -r nombre_biblioteca\n" \
                "o con:\n   sudo apt-get install python3-nombre_biblioteca")