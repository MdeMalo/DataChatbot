#!/usr/bin/python3
'''
Chatbot para calcular el ritmo de un corredor
'''

# Diccionario para almacenar registros de corredores
registros = {}

while True:
    entrada = input("Hola, soy el chatbot de running. Escribe {calcular} para calcular el ritmo, {agregar} para registrar un resultado, {consultar} para ver un registro o {salir} para terminar: \n").lower()

    if entrada == "calcular":
        try:
            distancia = float(input("Ingresa la distancia recorrida en kilómetros: "))
            tiempo = float(input("Ingresa el tiempo en minutos: "))
        except ValueError:
            print("Por favor, ingresa valores numéricos válidos.")
            continue

        if distancia == 0:
            print("La distancia no puede ser 0.")
        else:
            ritmo = tiempo / distancia
            print(f"El ritmo del corredor es: {ritmo:.2f} minutos por kilómetro.")

    elif entrada == "agregar":
        nombre = input("Ingresa el nombre del corredor: ")
        try:
            distancia = float(input("Ingresa la distancia recorrida en kilómetros: "))
            tiempo = float(input("Ingresa el tiempo en minutos: "))
        except ValueError:
            print("Por favor, ingresa valores numéricos válidos.")
            continue

        if distancia == 0:
            print("La distancia no puede ser 0.")
            continue

        ritmo = tiempo / distancia
        registros[nombre] = {"Distancia": distancia, "Tiempo": tiempo, "Ritmo": ritmo}
        print(f"Registro agregado correctamente para {nombre}.")

    elif entrada == "consultar":
        if not registros:
            print("No hay registros guardados.")
        else:
            nombre = input("Ingresa el nombre del corredor que deseas consultar: ")
            if nombre in registros:
                rec = registros[nombre]
                print(f"Registro de {nombre}:")
                print(f"  Distancia: {rec['Distancia']} km")
                print(f"  Tiempo: {rec['Tiempo']} minutos")
                print(f"  Ritmo: {rec['Ritmo']:.2f} minutos por km")
            else:
                print("Registro no encontrado.")

    elif entrada == "salir":
        print("Fin del programa.")
        break

    else:
        print("Comando no reconocido. Intenta de nuevo.")
