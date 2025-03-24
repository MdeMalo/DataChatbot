import requests
import subprocess
import shutil
import webbrowser
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
    
def buscar_youtube(busqueda):
    url = f"https://www.youtube.com/results?search_query={busqueda.replace(' ', '+')}"
    webbrowser.open(url)
    
def reproducir_en_spotify(cancion):
    url = f"https://open.spotify.com/search/{cancion.replace(' ', '%20')}"
    webbrowser.open(url)
    return f"Buscando '{cancion}' en Spotify..."
    
def mostrar_historial():
    archivo = './datos/historial_Chat.txt'
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
        comando = f'sudo dmidecode > ./datos/datos_bios.txt'
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            with open("./datos/datos_bios.txt", 'r', encoding='utf-8') as file:
                return file.write(resultado.stdout)
        else:
            return "Contraseña incorrecta."
    except Exception as e:
        return f"Error: {e}"
    
def info_lshw(tipo):
    try:
        comando = f'sudo lshw -C {tipo}> ./datos/datos_lshw.txt'
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            with open('./datos/datos_lshw.txt', 'r', encoding='utf-8') as file:
                return file.write(resultado.stdout)
        else:
            return "Error al obtener la información."
    except Exception as e:
        return f"Error: {e}"
    
def info_drivers():
    try:
        comando = 'sudo lspci -v > ./datos/datos_drivers.txt'
        subprocess.run(comando, shell=True)
        with open('./datos/datos_drivers.txt', 'r', encoding='utf-8') as file: 
            return file.read()
    except Exception as e:
        return f"Error: {e}"
    
def mostrar_drivers():
    archivo = './datos/datos_drivers.txt'
    ventana_drivers = tk.Tk()  # Crea una ventana secundaria
    ventana_drivers.title("Controladores del Sistema")
    ventana_drivers.geometry("800x600")  # Establece un tamaño mayor
    ventana_drivers.resizable(True, True)  # Permite redimensionar la ventana

    texto_drivers = scrolledtext.ScrolledText(ventana_drivers, width=100, height=20, wrap=tk.WORD)
    texto_drivers.pack(expand=True, fill='both')

    try:
        with open(archivo, 'r', encoding="utf-8") as file:
            contenido = file.read()
        if not contenido.strip():
            contenido = "El archivo está vacío."
        texto_drivers.insert(tk.INSERT, contenido)
        texto_drivers.config(state=tk.DISABLED)
    except FileNotFoundError:
        texto_drivers.insert(tk.INSERT, "El archivo 'historial_Chat.txt' no se encontró.")
        texto_drivers.config(state=tk.DISABLED)

def info_OS():
    try:
        subprocess.run("lsb_release -a > ./datos/datos_OS.txt", shell=True)
        with open('./datos/datos_OS.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error: {e}"

def imprimir_diccionarios(diccionario):
    resultado = ""
    for clave, valor in diccionario.items():
        resultado += f"{clave}: {valor}\n"
    return resultado

def imprimir_diccionarios_anidados(diccionario, nivel=0):
    resultado = ""
    indentacion = " " * (nivel * 4)  # Indentación para niveles anidados
    for clave, valor in diccionario.items():
        if isinstance(valor, dict):
            resultado += f"{indentacion}{clave}:\n"
            resultado += imprimir_diccionarios_anidados(valor, nivel + 1)
        elif isinstance(valor, list):
            resultado += f"{indentacion}{clave}:\n"
            for item in valor:
                if isinstance(item, dict):
                    resultado += imprimir_diccionarios_anidados(item, nivel + 1)
                else:
                    resultado += f"{indentacion}    {item}\n"
        else:
            resultado += f"{indentacion}{clave}: {valor}\n"
    return resultado

def imprimir_lista(lista):
    resultado = ""
    for item in lista:
        if isinstance(item, list):
            resultado += imprimir_lista(item)  # Llamada recursiva para listas anidadas
        else:
            resultado += f"{item}\n"
    return resultado