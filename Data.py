#!/usr/bin/python3
import csv
import time
import shutil
import os
import re
import random
import subprocess
import matplotlib.pyplot as plt
import requests
import sys
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
        
def mostrar_bibliotecas():
    archivo = 'requirements.txt'
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

def bus_en_txt(nombre, word):
    temperaturas = []
    try:
        with open(nombre, 'r', encoding='utf-8') as file:
            for numL, line in enumerate(file, 1):
                if word in line:
                    temp = float(line.split()[2].replace('°C', '').replace('+', ''))
                    temperaturas.append(temp)
        return sum(temperaturas) / len(temperaturas) if temperaturas else "No hay datos suficientes."
    except FileNotFoundError:
        return "Archivo no encontrado."
    
def bus_en_txt_info_OS(archivo):
    datos_OS = {}
    try:
        subprocess.run("lsb_release -a > datos_OS.txt", shell=True)
        with open('datos_OS.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if "Distributor ID" in line:
                    datos_OS["Distribuidor"] = line.split(":")[1].strip()
                elif "Description" in line:
                    datos_OS["Descripción"] = line.split(":")[1].strip()
                elif "Release" in line:
                    datos_OS["Versión"] = line.split(":")[1].strip()
                elif "Codename" in line:
                    datos_OS["Codename"] = line.split(":")[1].strip()
        return datos_OS
    except Exception as e:
        return f"Error: {e}"

def bus_en_txt_temperaturas_completas(nombre, word):
    temperaturas = []
    try:
        with open(nombre, 'r', encoding='utf-8') as file:
            for numL, line in enumerate(file, 1):
                if word in line:
                    temp = float(line.split()[2].replace('°C', '').replace('+', ''))
                    temperaturas.append(temp)
        return temperaturas
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []

def bus_en_txt_bios(nombre):
    datos_bios = []
    palabras_clave = ["Vendor", "Version", "Release Date"]

    vendor_encontrado = False 
    version_encontrada = False

    try:
        with open(nombre, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                # Evita leer más de un "Vendor"
                if "Vendor" in line:
                    if vendor_encontrado:
                        continue  # Ignora cualquier otro "Vendor" después del primero
                    vendor_encontrado = True
                    
                # Evita leer más de un "Version"
                if "Version" in line:
                    if version_encontrada:
                        continue
                    version_encontrada = True

                # Verifica si contiene "Version" o "Release Date" además del primer "Vendor"
                if any(palabra in line for palabra in palabras_clave):
                    datos_bios.append(line)

        if not datos_bios:
            print("No se encontraron datos relevantes en el archivo.")
        
        return datos_bios

    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []
    
def bus_en_txt_base_board(nombre):
    datos_base_board = []
    palabras_clave = ["Manufacturer", "Product Name", "Version", "Serial Number"]

    manufacturer_encontrado = False
    product_name_encontrado = False
    version_encontrada = False
    numero_serie_encontrado = False

    leyendo_seccion = False  # Para detectar cuándo empezar a leer

    try:
        with open(nombre, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                # Detectar el inicio de la sección "Base Board Information"
                if "Base Board Information" in line:
                    leyendo_seccion = True
                    continue  # Pasar a la siguiente línea y evitar que esta sea analizada

                # Si aún no estamos en la sección correcta, continuar con la siguiente línea
                if not leyendo_seccion:
                    continue

                # Buscar y agregar los datos clave evitando duplicados
                if "Manufacturer" in line and not manufacturer_encontrado:
                    datos_base_board.append(line)
                    manufacturer_encontrado = True
                    continue

                if "Product Name" in line and not product_name_encontrado:
                    datos_base_board.append(line)
                    product_name_encontrado = True
                    continue

                if "Version" in line and not version_encontrada:
                    datos_base_board.append(line)
                    version_encontrada = True
                    continue

                if "Serial Number" in line and not numero_serie_encontrado:
                    datos_base_board.append(line)
                    numero_serie_encontrado = True
                    continue

                # Si ya encontramos toda la información, salimos del bucle
                if manufacturer_encontrado and product_name_encontrado and version_encontrada and numero_serie_encontrado:
                    break

        if not datos_base_board:
            print("No se encontraron datos relevantes en el archivo.")

        return datos_base_board

    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []

import re

def bus_en_txt_lshw_cpu(nombre):
    datos_cpu = {}
    palabras_clave = {
        "producto": r"(?i)^\s*(producto|product)\s*:\s*(.+)",
        "fabricante": r"(?i)^\s*(fabricante|vendor)\s*:\s*(.+)",
        "versión": r"(?i)^\s*(versión|version)\s*:\s*(.+)",
        "serial": r"(?i)^\s*(serial|número de serie)\s*:\s*(.+)",
        "ranura": r"(?i)^\s*(ranura|slot)\s*:\s*(.+)"
    }

    leyendo_seccion = False  # Para detectar cuándo empezar a leer

    try:
        with open(nombre, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                # Detectar el inicio de la sección "CPU"
                if re.match(r"^\s*\*\-cpu", line, re.IGNORECASE):
                    leyendo_seccion = True
                    continue  # Evita procesar la línea de detección

                # Si aún no estamos en la sección correcta, continuar con la siguiente línea
                if not leyendo_seccion:
                    continue

                # Buscar y extraer los datos clave
                for clave, patron in palabras_clave.items():
                    match = re.match(patron, line)
                    if match and clave not in datos_cpu:
                        datos_cpu[clave] = match.group(2).strip()
                        break  # Evita procesar más claves en la misma línea

                # Si ya encontramos toda la información, salimos del bucle
                if len(datos_cpu) == len(palabras_clave):
                    break

        return datos_cpu if datos_cpu else {"Error": "No se encontraron datos relevantes."}

    except FileNotFoundError:
        return {"Error": "Archivo no encontrado."}
    except Exception as e:
        return {"Error": f"Error inesperado: {e}"}

def bus_en_txt_lshw_ram(nombre):
    datos_ram = {"tamaño_total": "", "modulos": []}
    patron_tamano_total = r"(?i)^\s*tamaño\s*:\s*(\d+\S+)"
    patrones_modulo = {
        "descripción": r"(?i)^\s*descripción\s*:\s*(.+)",  # Agregado correctamente
        "producto": r"(?i)^\s*producto\s*:\s*(.+)",
        "fabricante": r"(?i)^\s*(fabricante|vendor)\s*:\s*(.+)",
        "serial": r"(?i)^\s*(serial|número de serie)\s*:\s*(.+)",
        "ranura": r"(?i)^\s*(ranura|slot)\s*:\s*(.+)",
        "tamaño": r"(?i)^\s*tamaño\s*:\s*(.+)",
        "reloj": r"(?i)^\s*reloj\s*:\s*(.+)"
    }

    leyendo_memoria = False
    leyendo_modulo = False
    modulo_actual = {}

    try:
        with open(nombre, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                # Detectar el inicio de la sección de memoria total
                if re.match(r"^\s*\*\-memory", line, re.IGNORECASE):
                    leyendo_memoria = True
                    continue

                # Capturar el tamaño total de RAM
                if leyendo_memoria and not datos_ram["tamaño_total"]:
                    match_total = re.search(patron_tamano_total, line)
                    if match_total:
                        datos_ram["tamaño_total"] = match_total.group(1)
                        continue

                # Detectar el inicio de un módulo de RAM
                if re.match(r"^\s*\*\-bank:\d+", line, re.IGNORECASE):
                    leyendo_modulo = True
                    if modulo_actual:  # Guardar el módulo anterior si ya hay datos
                        datos_ram["modulos"].append(modulo_actual)
                    modulo_actual = {}  # Reiniciar el módulo actual
                    continue

                # Capturar datos del módulo RAM
                if leyendo_modulo:
                    for clave, patron in patrones_modulo.items():
                        match = re.search(patron, line)
                        if match and clave not in modulo_actual:
                            modulo_actual[clave] = match.group(1).strip()
                            break  # Evita procesar más claves en la misma línea

        # Guardar el último módulo detectado
        if modulo_actual:
            datos_ram["modulos"].append(modulo_actual)

        return datos_ram if datos_ram["tamaño_total"] or datos_ram["modulos"] else {"Error": "No se encontraron datos relevantes."}

    except FileNotFoundError:
        return {"Error": "Archivo no encontrado."}
    except Exception as e:
        return {"Error": f"Error inesperado: {e}"}
    
def leer_datos_csv(archivo):
    registros = []
    try:
        with open(archivo, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 1:
                    try:
                        uso_disco = float(row[0])
                        temperaturas = [float(temp) for temp in row[1:]]
                        registros.append((uso_disco, temperaturas))
                    except ValueError:
                        continue
    except FileNotFoundError:
        print("El archivo no existe.")
    return registros

def guardar_en_csv(temperaturas, archivo):
    if not temperaturas:
        print("No hay datos para guardar en CSV.")
        return

    # Leer los datos existentes
    registros = []
    try:
        with open(archivo, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            registros = [row for row in reader if row]  # Filtrar filas vacías
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe. Se creará uno nuevo.")

    # Agregar la nueva línea con el uso de disco
    uso_disco = obtener_espacio_disco()
    nueva_fila = [uso_disco] + temperaturas
    registros.append(nueva_fila)

    # Mantener solo los últimos 60 registros
    registros = registros[-60:]

    # Escribir los datos actualizados al archivo
    with open(archivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(registros)


def graficar_temperaturas(registros):
    if not registros:
        print("No hay registros para graficar.")
        return

    fig, ax1 = plt.subplots()
    num_nucleos = len(registros[0][1])
    series_temperaturas = [[] for _ in range(num_nucleos)]

    for _, temps in registros:
        for i in range(num_nucleos):
            series_temperaturas[i].append(temps[i])

    x = list(range(1, len(registros) + 1))

    for i in range(num_nucleos):
        ax1.plot(x, series_temperaturas[i], marker='o', label=f'Núcleo {i+1}')
    
    ax1.set_xlabel('Registro')
    ax1.set_ylabel('Temperatura (°C)')
    ax1.grid(True)
    ax1.legend(loc='upper left')

    plt.show()

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
    
def comprobar_Archivos():
    if not os.path.exists("temp.txt"):
        with open("temp.txt", 'w', encoding='utf-8') as file:
            pass

    if not os.path.exists("datos_temperaturas.csv"):
        with open("datos_temperaturas.csv", 'w', encoding='utf-8') as file:
            pass
        
    if not os.path.exists("datos_bios.txt"):
        with open("datos_bios.txt", 'w', encoding='utf-8') as file:
            pass
        
    if not os.path.exists("datos_lshw.txt"):
        with open("datos_lshw.txt", 'w', encoding='utf-8') as file:
            pass
        
    if not os.path.exists("datos_OS.txt"):
        with open("datos_OS.txt", 'w', encoding='utf-8') as file:
            pass
        
    if not os.path.exists("historial_Chat.txt"):
        with open("historial_Chat.txt", 'w', encoding='utf-8') as file:
            pass
        
    if not os.path.exists("requirements.txt"):
        with open("requirements.txt", 'w', encoding='utf-8') as file:
            file.write("Las bibliotecas necesarias son: \ncsv\ntime\nshutil\nos\nre\nrandom\nsubprocess\n" \
                "matplotlib\nrequests\nsys\ntkinter\nPueden ser inctaladas con:\n   pip install -r nombre_biblioteca\n" \
                "o con:\n   sudo apt-get install python3-nombre_biblioteca")

def respuestas_chat(entrada_usuario):
    entrada_usuario = entrada_usuario.lower()

    entradas = {
        "saludos": r"\b(hola|hey|qué tal|buenos días|buenas tardes)\b",
        "despedidas": r"\b(adiós|bye|hasta luego|nos vemos)\b",
        "hora": r"\b(qué hora es|hora actual|dime la hora)\b",
        "clima": r"\b(cómo está el clima|qué tiempo hace|clima de hoy|clima)\b",
        "espacio_disco": r"\b(espacio en disco|cuánto espacio tengo libre|cuánto espacio tengo ocupado|espacio ocupado)\b",
        "espacio_libre": r"\b(espacio libre|cuánto espacio tengo disponible)\b",
        "espacio_total": r"\b(espacio total|cuánto espacio tengo en total)\b",
        "promedio_temperaturas": r"\b(promedio de temperaturas)\b",
        "graficar_temperaturas": r"\b(graficar temperaturas|grafica)\b",
        "info_bios": r"\b(info bios|dame informacion de la bios|bios)\b",
        "base_board": r"\b(base board|placa base|informacion placa base|información placa base|placa madre)\b",
        "cpu_info": r"\b(cpu info|informacion cpu|información cpu|cpu)\b",
        "memoria_info": r"\b(informacion de memoria|ram|memoria ram)\b",
        "sistema_operativo": r"\b(sistema operativo|qué sistema operativo tengo)\b",
        "historial": r"\b(historial|mostrar historial)\b",
        "ayuda": r"\b(que puedes hacer|ayuda)\b",
        "Bibliotecas": r"\b(bibliotecas|paquetes)\b"
    }

    if re.search(entradas["saludos"], entrada_usuario):
        return random.choice(["¡Hola! ¿En qué puedo ayudarte?", "¡Hey! ¿En qué puedo ayudarte?"])
    elif re.search(entradas["despedidas"], entrada_usuario):
        return "¡Hasta luego! Que tengas un buen día."
    elif re.search(entradas["hora"], entrada_usuario):
        return f"La hora actual es {time.strftime('%H:%M')}."
    elif re.search(entradas["clima"], entrada_usuario):
        ciudad = input("¿De qué ciudad quieres saber el clima?: ")
        return obtener_clima(ciudad)
    elif re.search(entradas["espacio_disco"], entrada_usuario):
        return f"Tienes {obtener_espacio_disco()}% de espacio en disco ocupado."
    elif re.search(entradas["espacio_libre"], entrada_usuario):
        return f"Tienes {obtener_espacio_libre()}% de espacio en disco libre."
    elif re.search(entradas["espacio_total"], entrada_usuario):
        return f"Tienes un total de {obtener_espacio_total()} bytes de espacio en disco."
    elif re.search(entradas["promedio_temperaturas"], entrada_usuario):
        os.system("sensors >temp.txt")
        return f"El promedio de todas las temperaturas es {bus_en_txt('temp.txt', 'Core')}°C."
    elif re.search(entradas["graficar_temperaturas"], entrada_usuario):
        os.system("sensors >temp.txt")
        temps = bus_en_txt_temperaturas_completas('temp.txt', 'Core')
        guardar_en_csv(temps, 'datos_temperaturas.csv')
        registros = leer_datos_csv("datos_temperaturas.csv")
        if registros:
            graficar_temperaturas(registros)
            return "Se ha generado la gráfica de temperaturas."
        else:
            return "No hay datos suficientes para graficar."
    elif re.search(entradas["info_bios"], entrada_usuario):
        info_bios()
        return f"Aqui tienes alguna informacion importante de tu bios {bus_en_txt_bios('datos_bios.txt')}"
    elif re.search(entradas["base_board"], entrada_usuario):
        info_bios()
        return f"Aqui tienes alguna informacion importante de tu placa base {bus_en_txt_base_board('datos_bios.txt')}"
    elif re.search(entradas["cpu_info"], entrada_usuario):
        info_lshw("cpu")
        return f"Aqui tienes alguna informacion importante de tu cpu {bus_en_txt_lshw_cpu('datos_lshw.txt')}"
    elif re.search(entradas["memoria_info"], entrada_usuario):
        info_lshw("memory")
        return f"Aqui tienes alguna informacion importante de tu memoria {bus_en_txt_lshw_ram('datos_lshw.txt')}"
    elif re.search(entradas["sistema_operativo"], entrada_usuario):
        info_OS()
        return f"Aqui tienes alguna informacion importante de tu sistema operativo {bus_en_txt_info_OS('datos_OS.txt')}"
    elif re.search(entradas["historial"], entrada_usuario):
        mostrar_historial()
        return "Historial abierto en ventana emergente."
    elif re.search(entradas["Bibliotecas"], entrada_usuario):
        mostrar_bibliotecas()
        return "Bibliotecas necesarias abiertas en ventana emergente."
    elif re.search(entradas["ayuda"], entrada_usuario):
        return "Puedo ayudarte con las siguientes tareas:\n" \
               "- Saludos y despedidas\n" \
               "- Decirte la hora actual\n" \
               "- Obtener el clima de una ciudad\n" \
               "- Mostrar el espacio en disco\n" \
               "- Mostrar el espacio libre en disco\n" \
               "- Mostrar el espacio total en disco\n" \
               "- Calcular el promedio de temperaturas\n" \
               "- Graficar temperaturas\n" \
               "- Obtener información de la BIOS\n" \
               "- Obtener información de la placa base\n" \
               "- Obtener información de la CPU\n" \
               "- Obtener información de la memoria RAM\n" \
               "- Obtener información del sistema operativo\n" \
               "- Mostrar el historial del chat\n" \
               "- Mostrar las bibliotecas necesarias (si no estan instaladas se intalaran automaticamente)\n" \
                   "    Pero si no se instalan, puedes verlas escribiendo BIBLIOTECAS\n"
    else:
        return random.choice(["No entiendo tu mensaje, ¿puedes reformularlo?", "Interesante, pero no sé cómo responder a eso."])

def main():    
    comprobar_e_instalar_paquetes()
    comprobar_Archivos()
    historial = 'historial_Chat.txt'
    bienvenida = "¡Hola! Soy Data. Puedo ayudarte con algunas tareas."
    
    with open(historial, "a", encoding="utf-8") as file:
        file.write("Historial del chat:\n")
        file.write(f"Data: {bienvenida}\n")
    
    print(bienvenida)
    
    while True:
        user_text = input("Tú: ")
        if user_text.lower() in ["adiós", "bye", "hasta luego", "nos vemos", "cerrar", "salir", "exit", "quit", "adios"]:
            print("Data: Adiós, Capitán. Espero que nuestra próxima interacción sea igualmente productiva.")
            with open(historial, "a", encoding="utf-8") as file:
                file.write("Data: Adiós, Capitán. Espero que nuestra próxima interacción sea igualmente productiva.\n")  # Guarda el mensaje de despedida
            break
        
        respuesta = respuestas_chat(user_text)  # Se guarda la respuesta en una variable
        print("Data:", respuesta)

        with open(historial, "a", encoding="utf-8") as file:
            file.write(f"Tú: {user_text}\n")
            file.write(f"Bot: {respuesta}\n")
            
    with open(historial, "a", encoding="utf-8") as file:
        file.write(f"Fin del historial.\n")
        file.write("-----------------------------------------------------\n")


if __name__ == "__main__":
    main()
