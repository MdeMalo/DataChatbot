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
        "saludos": r"\b(hola|hey|qué tal|buenos días|buenas tardes|buenas noches|qué onda|holi|saludos)\b",
        "despedidas": r"\b(adiós|bye|hasta luego|nos vemos|chao|hasta pronto|cuídate|nos vemos luego)\b",
        "hora": r"\b(qué hora es|hora actual|dime la hora|me puedes decir la hora|hora exacta|sabes qué hora es|hora)\b",
        "clima": r"\b(cómo está el clima|qué tiempo hace|clima de hoy|estado del tiempo|pronóstico|tiempo actual|temperatura actual|clima)\b",
        "espacio_disco": r"\b(espacio en disco|cuánto espacio tengo libre|cuánto espacio tengo ocupado|espacio ocupado|espacio de disco|capacidad de disco|uso de almacenamiento|disco usado)\b",
        "espacio_libre": r"\b(espacio libre|cuánto espacio tengo disponible|disponible|espacio disponible)\b",
        "espacio_total": r"\b(espacio total|cuánto espacio tengo en total|capacidad total|total de disco)\b",
        "promedio_temperaturas": r"\b(promedio de temperaturas|media de temperaturas|temperatura promedio|temperatura media|temperaturas)\b",
        "graficar_temperaturas": r"\b(graficar temperaturas|grafica|mostrar gráfico de temperaturas|plotear temperaturas|dibujar gráfica de temperaturas)\b",
        "info_bios": r"\b(info bios|dame informacion de la bios|bios|información de la BIOS|datos BIOS|bios info)\b",
        "base_board": r"\b(base board|placa base|informacion placa base|información placa base|placa madre|motherboard|tarjeta madre)\b",
        "cpu_info": r"\b(cpu info|informacion cpu|información cpu|cpu|procesador|proce|información del procesador|info del CPU|procesador info)\b",
        "memoria_info": r"\b(informacion de memoria|ram|memoria ram|memoria|información de RAM|datos de memoria|info de RAM)\b",
        "sistema_operativo": r"\b(sistema operativo|qué sistema operativo tengo|so|os|sistema de operación|nombre del sistema operativo|OS info)\b",
        "historial": r"\b(historial|mostrar historial|ver historial|mostrar registros|lista de interacciones)\b",
        "ayuda": r"\b(que puedes hacer|ayuda|asistencia|comandos disponibles|cómo me puedes ayudar)\b",
        "Bibliotecas": r"\b(bibliotecas|paquetes|librerias|librerías|módulos|frameworks|dependencias)\b",
        "Controladores": r"\b(controladores|drivers|drivers de hardware|drivers de dispositivo|drivers de sistema)\b",
        "youtube": r"\b(youtube|busca en youtube|yutu|busqueda de youtube)\b",
        "spotify": r"\b(spotify|musica|pon musica|música|pon música)\b"
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
        espacio_total_bytes = fb.obtener_espacio_total()
        espacio_total_megas = espacio_total_bytes / (1024 * 1024)
        espacio_total_gigas = espacio_total_bytes / (1024 * 1024 * 1024)
        return f"Tienes un total de {espacio_total_bytes} bytes ({espacio_total_megas:.2f} MB / {espacio_total_gigas:.2f} GB) de espacio en disco."
    elif re.search(entradas["promedio_temperaturas"], entrada_usuario):
        os.system("sensors > ./datos/temp.txt")
        return f"El promedio de todas las temperaturas es {bt.bus_en_txt('./datos/temp.txt', 'Core')}°C."
    elif re.search(entradas["graficar_temperaturas"], entrada_usuario):
        os.system("sensors > ./datos/temp.txt")
        temps = bt.bus_en_txt_temperaturas_completas('./datos/temp.txt', 'Core')
        bcsv.guardar_en_csv(temps, './datos/datos_temperaturas.csv')
        registros = bcsv.leer_datos_csv("./datos/datos_temperaturas.csv")
        if registros:
            bcsv.graficar_temperaturas(registros)
            return "Se ha generado la gráfica de temperaturas."
        else:
            return "No hay datos suficientes para graficar."
    elif re.search(entradas["info_bios"], entrada_usuario):
        fb.info_bios()
        return f"Aqui tienes alguna informacion importante de tu bios\n{fb.imprimir_lista(bt.bus_en_txt_bios('./datos/datos_bios.txt'))}"
    elif re.search(entradas["base_board"], entrada_usuario):
        fb.info_bios()
        return f"Aqui tienes alguna informacion importante de tu placa base\n{fb.imprimir_lista(bt.bus_en_txt_base_board('./datos/datos_bios.txt'))}"
    elif re.search(entradas["cpu_info"], entrada_usuario):
        fb.info_lshw("cpu")
        return f"Aqui tienes alguna informacion importante de tu cpu:\n{fb.imprimir_diccionarios(bt.bus_en_txt_lshw_cpu('./datos/datos_lshw.txt'))}"
    elif re.search(entradas["memoria_info"], entrada_usuario):
        fb.info_lshw("memory")
        return f"Aqui tienes alguna informacion importante de tu memoria {fb.imprimir_diccionarios_anidados(bt.bus_en_txt_lshw_ram('./datos/datos_lshw.txt'))}"
    elif re.search(entradas["sistema_operativo"], entrada_usuario):
        fb.info_OS()
        return f"Aqui tienes alguna informacion importante de tu sistema operativo:\n{fb.imprimir_diccionarios(bt.bus_en_txt_info_OS('./datos/datos_OS.txt'))}"
    elif re.search(entradas["historial"], entrada_usuario):
        fb.mostrar_historial()
        return "Historial abierto en ventana emergente."
    elif re.search(entradas["Bibliotecas"], entrada_usuario):
        ip.mostrar_bibliotecas()  # CAMBIAR A FUTURO
        return "Bibliotecas necesarias abiertas en ventana emergente."
    elif re.search(entradas["Controladores"], entrada_usuario):
        fb.info_drivers()
        fb.mostrar_drivers()
        return "Controladores abiertos en ventana emergente."
    elif re.search(entradas["youtube"], entrada_usuario):
        busqueda = input("¿Qué deseas buscar?\nTu:")
        fb.buscar_youtube(busqueda)
        return f"Buscando {busqueda} en navegdor"
    elif re.search(entradas["spotify"], entrada_usuario):
        busqueda = input("¿Qué deseas buscar?\nTu:")
        fb.reproducir_en_spotify(busqueda)
        return f"Buscando {busqueda} en spotify"
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
               "- También puedo ayudarte a reproducir música en spotify y YouTube\n" \
               "- Mostrar las bibliotecas necesarias (si no estan instaladas se intalaran automaticamente)\n" \
                   "    Pero si no se instalan, puedes verlas escribiendo BIBLIOTECAS\n"
    else:
        return random.choice(["No entiendo tu mensaje, ¿puedes reformularlo?", "Interesante, pero no sé cómo responder a eso.", "No pude entender eso, si necesitas ayuda puedes escribir AYUDA."])
