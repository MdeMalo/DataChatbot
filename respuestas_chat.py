import re
import random
import time
import os
import funciones_Basicas as fb
import instalar_paquetes as ip
import buscar_textos as bt
import buscar_csv as bcsv

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
        return fb.obtener_clima(ciudad)
    elif re.search(entradas["espacio_disco"], entrada_usuario):
        return f"Tienes {fb.obtener_espacio_disco()}% de espacio en disco ocupado."
    elif re.search(entradas["espacio_libre"], entrada_usuario):
        return f"Tienes {fb.obtener_espacio_libre()}% de espacio en disco libre."
    elif re.search(entradas["espacio_total"], entrada_usuario):
        return f"Tienes un total de {fb.obtener_espacio_total()} bytes de espacio en disco."
    elif re.search(entradas["promedio_temperaturas"], entrada_usuario):
        os.system("sensors >temp.txt")
        return f"El promedio de todas las temperaturas es {bt.bus_en_txt('temp.txt', 'Core')}°C."
    elif re.search(entradas["graficar_temperaturas"], entrada_usuario):
        os.system("sensors >temp.txt")
        temps = bt.bus_en_txt_temperaturas_completas('temp.txt', 'Core')
        bcsv.guardar_en_csv(temps, 'datos_temperaturas.csv')
        registros = bcsv.leer_datos_csv("datos_temperaturas.csv")
        if registros:
            bcsv.graficar_temperaturas(registros)
            return "Se ha generado la gráfica de temperaturas."
        else:
            return "No hay datos suficientes para graficar."
    elif re.search(entradas["info_bios"], entrada_usuario):
        fb.info_bios()
        return f"Aqui tienes alguna informacion importante de tu bios {bt.bus_en_txt_bios('datos_bios.txt')}"
    elif re.search(entradas["base_board"], entrada_usuario):
        fb.info_bios()
        return f"Aqui tienes alguna informacion importante de tu placa base {bt.bus_en_txt_base_board('datos_bios.txt')}"
    elif re.search(entradas["cpu_info"], entrada_usuario):
        fb.info_lshw("cpu")
        return f"Aqui tienes alguna informacion importante de tu cpu {bt.bus_en_txt_lshw_cpu('datos_lshw.txt')}"
    elif re.search(entradas["memoria_info"], entrada_usuario):
        fb.info_lshw("memory")
        return f"Aqui tienes alguna informacion importante de tu memoria {bt.bus_en_txt_lshw_ram('datos_lshw.txt')}"
    elif re.search(entradas["sistema_operativo"], entrada_usuario):
        fb.info_OS()
        return f"Aqui tienes alguna informacion importante de tu sistema operativo {bt.bus_en_txt_info_OS('datos_OS.txt')}"
    elif re.search(entradas["historial"], entrada_usuario):
        fb.mostrar_historial()
        return "Historial abierto en ventana emergente."
    elif re.search(entradas["Bibliotecas"], entrada_usuario):
        ip.mostrar_bibliotecas()  # CAMBIAR A FUTURO
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
