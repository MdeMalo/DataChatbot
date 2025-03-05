import requests
import subprocess
import shutil
import tkinter as tk
from tkinter import scrolledtext

def obtener_clima(ciudad):
    datos_clima = {}

    API_key = "991d0598ada0fc2774d261626d556e03"
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_key}&units=metric&lang=es"

    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        
        datos_clima["ciudad"] = ciudad
        datos_clima["descripcion"] = data["weather"][0]["description"]
        datos_clima["temperatura"] = data["main"]["temp"]
        datos_clima["humedad"] = data["main"]["humidity"]
        datos_clima["viento"] = data["wind"]["speed"]
    
    else:
        datos_clima["error"] = f"Error {response.status_code}: No se pudo obtener el clima."

    return datos_clima
        
    #     print(f"Claro, aquí tienes la información del clima en {ciudad}:")
    #     print("Clima actual:", weather_description)
    #     print("Temperatura actual:", current_temperature, "°C")
    # else:
    #     print("Error en la solicitud:", response.status_code)
    
def mostrar_historial():
    archivo = 'historial_Chat.txt'
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
        texto_historial.insert(tk.INSERT, "El archivo 'historial_Chat.txt' no se encontró.")
        texto_historial.config(state=tk.DISABLED)

def obtener_espacio_disco():
    total, usado, libre = shutil.disk_usage("/")
    return round((usado / total) * 100, 2)

def obtener_espacio_libre():
    total, usado, libre = shutil.disk_usage("/")
    return round((libre / total) * 100, 2)

def obtener_espacio_total():
    total, _, _ = shutil.disk_usage("/")
    return total

def info_bios(): 
    try:
        comando = f'sudo dmidecode > datos_bios.txt'
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            with open("datos_bios.txt", 'r', encoding='utf-8') as file:
                return file.write(resultado.stdout)
        else:
            return "Contraseña incorrecta."
    except Exception as e:
        return f"Error: {e}"
    
def info_lshw(tipo):
    try:
        comando = f'sudo lshw -C {tipo}> datos_lshw.txt'
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            with open('datos_lshw.txt', 'r', encoding='utf-8') as file:
                return file.write(resultado.stdout)
        else:
            return "Error al obtener la información."
    except Exception as e:
        return f"Error: {e}"

def info_OS():
    try:
        subprocess.run("lsb_release -a > datos_OS.txt", shell=True)
        with open('datos_OS.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error: {e}"
