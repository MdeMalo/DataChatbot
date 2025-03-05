import csv
import matplotlib.pyplot as plt
import funciones_Basicas as fb

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

    uso_disco = fb.obtener_espacio_disco()

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
