#!/usr/bin/python3
import instalar_paquetes as ip
import respuestas_chat as rc

def main():    
    ip.comprobar_e_instalar_paquetes()
    ip.comprobar_Archivos()
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
        
        respuesta = rc.respuestas_chat(user_text)  # Se guarda la respuesta en una variable
        print("Data:", respuesta)

        with open(historial, "a", encoding="utf-8") as file:
            file.write(f"Tú: {user_text}\n")
            file.write(f"Bot: {respuesta}\n")
            
    with open(historial, "a", encoding="utf-8") as file:
        file.write(f"Fin del historial.\n")
        file.write("-----------------------------------------------------\n")


if __name__ == "__main__":
    main()
