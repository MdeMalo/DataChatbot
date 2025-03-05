import subprocess
import re

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
        subprocess.run("lsb_release -a > ./datos/datos_OS.txt", shell=True)
        with open('./datos/datos_OS.txt', 'r', encoding='utf-8') as file:
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
