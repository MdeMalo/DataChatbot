Data – Chatbot de Asistencia en Python

Este repositorio contiene un chatbot desarrollado en Python que te ayuda con diversas tareas del sistema y otras consultas.
El proyecto incorpora funcionalidades para obtener información del clima, uso de disco, temperaturas, datos de la BIOS, placa base, CPU, memoria, sistema operativo, y más. Además, incluye funciones para instalar automáticamente los paquetes necesarios (en sistemas basados en apt) y guarda el historial del chat en un archivo.

Características

Interacción en lenguaje natural:
El chatbot reconoce saludos, despedidas, consultas sobre el clima, información del sistema y muchas otras peticiones mediante expresiones regulares.

Consultas sobre el sistema:

Obtener información de la BIOS, placa base, CPU y memoria RAM.
Consultar el uso, espacio libre y total del disco.
Obtener datos del sistema operativo.

Consultas sobre el clima:

Solicita el clima de una ciudad (aunque la petición de ciudad se realiza vía terminal, se recomienda integrarla en una interfaz en el futuro).

Manejo de temperaturas:

Calcular promedios y graficar temperaturas utilizando matplotlib.

Historial del chat:

Se guarda la conversación en el archivo historial_Chat.txt y puedes visualizarlo mediante una ventana emergente con Tkinter.

Instalación automática de dependencias:

Si faltan paquetes (como matplotlib, requests o tkinter), el script intenta instalarlos usando apt (requiere privilegios de administrador).


Requisitos:

Python 3.x

Sistema basado en apt (por ejemplo, Ubuntu, Debian) para la instalación automática de paquetes.

Las siguientes bibliotecas de Python:

csv, time, shutil, os, re, random, subprocess, matplotlib, requests, sys, tkinter.

Para ejecutar los comandos de consola que utiliza el proyecto, deberás tener instalados algunos paquetes del sistema. En concreto, se requieren:

lm-sensors: Proporciona el comando sensors para monitorear temperaturas y otros sensores.

dmidecode: Permite obtener información detallada de la BIOS y hardware.

lshw: Sirve para listar el hardware del sistema, útil para extraer datos de CPU y memoria.

lsb-release: Proporciona el comando lsb_release para obtener información del sistema operativo.


Instalación:

    1.-Clona el repositorio:
        git clone https://github.com/tuusuario/DataChatbot.git
        cd DataChatbot
    2.- (Opcional) Revisa o instala las dependencias:
        El script intentará instalar automáticamente los paquetes necesarios mediante sudo apt install python3-nombre_del_paquete y para los comandos de consola sudo apt update y sudo apt install lm-sensors dmidecode lshw lsb-release, pero también puedes instalarlos manualmente si lo prefieres.
        
    3.- Ejecuta el chatbot:
        Para iniciar el chatbot en modo consola, ejecuta:
        "python3 Data.py" aunque también cuenta con shebang y tambien funciona con "./Data.py "
        Si deseas usar la interfaz gráfica para ver el historial (o integrarla), asegúrate de tener Tkinter instalado y ejecuta el script según tus preferencias.

Uso:

    1.- Al iniciar el script, se mostrará un mensaje de bienvenida y se guardará en el historial.
    2.- Escribe tus consultas en la terminal; el chatbot responderá según la entrada proporcionada.
    3.- Para finalizar la conversación, escribe palabras como adiós, bye, salir, exit, etc.
    4.- El historial de la conversación se guarda en el archivo historial_Chat.txt y puedes visualizarlo con la opción "Mostrar Historial" en la interfaz gráfica.

Estructura del Proyecto:

    DataChatbot/
    │
    ├── Data.py              # Script principal del chatbot (modo consola)
    ├── datos_bios.txt           #Archivo donde se guarda la info de la Bios
    ├── datos_lshw.txt           # Archivo donde se guarda cada salida del comando lshw
    ├── datos_OS.txt             # Archivo donde se guarda la info del sistema operativo
    ├── datos_temperaturas.csv   # Archivo donde se guarda los datos de temperaturas en formato csv para grafica
    ├── historial_Chat.txt       # Archivo donde se guarda el historial del chat
    ├── requirements.txt         # Archivo que lista las bibliotecas necesarias (se genera automáticamente si no existe)
    ├── temp.txt                 #Archivo donde se guarda la salida del comando sensors
    └── README.md                # Este archivo

