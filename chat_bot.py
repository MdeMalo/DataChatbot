#!/usr/bin/python3
import csv
import time
import shutil
import os
import re
import random
import subprocess
import matplotlib.pyplot as plt

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

def info_bios(contraseña_usuario): 
    try:
        comando = f'echo {contraseña_usuario} | sudo dmidecode > datos_bios.txt'
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            with open("datos_bios.txt", 'r', encoding='utf-8') as file:
                return file.write(resultado.stdout)
        else:
            return "Contraseña incorrecta."
    except Exception as e:
        return f"Error: {e}"
    

def respuestas_chat(entrada_usuario):
    entrada_usuario = entrada_usuario.lower()

    entradas = {
        "saludos": r"\b(hola|hey|qué tal|buenos días|buenas tardes)\b",
        "despedidas": r"\b(adiós|bye|hasta luego|nos vemos)\b",
        "hora": r"\b(qué hora es|hora actual|dime la hora)\b",
        "clima": r"\b(cómo está el clima|qué tiempo hace|clima de hoy)\b",
        "espacio_disco": r"\b(espacio en disco|cuánto espacio tengo libre|cuánto espacio tengo ocupado|espacio ocupado)\b",
        "espacio_libre": r"\b(espacio libre|cuánto espacio tengo disponible)\b",
        "espacio_total": r"\b(espacio total|cuánto espacio tengo en total)\b",
        "promedio_temperaturas": r"\b(promedio de temperaturas)\b",
        "graficar_temperaturas": r"\b(graficar temperaturas|grafica)\b",
        "info_bios": r"\b(info bios|dame informacion de la bios|bios)\b",
        "base_board": r"\b(base board|placa base|informacion placa base|información placa base)\b"
    }

    if re.search(entradas["saludos"], entrada_usuario):
        return random.choice(["¡Hola! ¿En qué puedo ayudarte?", "¡Hey! ¿En qué puedo ayudarte?"])
    elif re.search(entradas["despedidas"], entrada_usuario):
        return "¡Hasta luego! Que tengas un buen día."
    elif re.search(entradas["hora"], entrada_usuario):
        return f"La hora actual es {time.strftime('%H:%M')}."
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
        contrasela_usuario = input("Introduce tu contraseña de usuario: ")
        info_bios(contrasela_usuario)
        return f"Aqui tienes alguna informacion importante de tu bios {bus_en_txt_bios('datos_bios.txt')}"
    elif re.search(entradas["base_board"], entrada_usuario):
        contrasela_usuario = input("Introduce tu contraseña de usuario: ")
        info_bios(contrasela_usuario)
        return f"Aqui tienes alguna informacion importante de tu placa base {bus_en_txt_base_board('datos_bios.txt')}"
    else:
        return random.choice(["No entiendo tu mensaje, ¿puedes reformularlo?", "Interesante, pero no sé cómo responder a eso."])

def main():    
    if not os.path.exists("temp.txt"):
        with open("temp.txt", 'w', encoding='utf-8') as file:
            pass  # Se crea un archivo vacío

    if not os.path.exists("datos_temperaturas.csv"):
        with open("datos_temperaturas.csv", 'w', encoding='utf-8') as file:
            pass  # Se crea un archivo vacío
        
    if not os.path.exists("datos_bios.txt"):
        with open("datos_bios.txt", 'w', encoding='utf-8') as file:
            pass
    
    while True:
        user_text = input("Tú: ")
        if user_text.lower() in ["adiós", "bye", "hasta luego", "nos vemos"]:
            print("Chatbot: ¡Hasta luego!")
            break
        print("Chatbot:", respuestas_chat(user_text))

if __name__ == "__main__":
    main()
