## \file main.py
#  \brief Este archivo contiene la lógica principal para procesar un conjunto de ciudades desde un archivo, generar la matriz de distancias y ejecutar un algoritmo greedy.

import os
from Ciudad import Ciudad
from Mapa import Mapa


## \brief Función para listar todos los archivos que contiene una carpeta.
#
#  Esta función busca todos los archivos en un directorio específico y devuelve una lista con sus rutas completas.
#
#  \param carpeta La ruta del directorio en el que se buscan archivos.
#  \return Una lista con los archivos encontrados en la carpeta.
#
def buscarCarpeta(carpeta):
    contenidoCarpeta = []
    # Itera sobre los archivos en el directorio proporcionado
    for archivo in os.listdir(carpeta):
        ruta = os.path.join(carpeta, archivo)
        # Verifica si es un archivo y no un directorio
        if os.path.isfile(ruta):
            contenidoCarpeta.append(ruta)
    return contenidoCarpeta


## \brief Función para que el usuario seleccione un archivo de una lista.
#
#  Presenta al usuario una lista de archivos y le permite seleccionar uno.
#
#  \param contenidoCarpeta Una lista con las rutas de los archivos disponibles.
#  \return La ruta completa del archivo seleccionado por el usuario.
#
def selecciona_archivo(contenidoCarpeta):
    print("Listando los archivos TSP disponibles en el directorio:")
    # Extrae solo los nombres de archivo de las rutas
    nombres_archivos = [os.path.basename(archivo) for archivo in contenidoCarpeta]
    # Muestra los archivos disponibles con su número correspondiente
    for i, archivo in enumerate(nombres_archivos):
        print(f"    {i + 1}................... {archivo}")
    # Solicita al usuario que seleccione un archivo
    while True:
        try:
            seleccion = int(input("Seleccione el número del archivo que desea procesar: "))
            # Verifica que la selección sea válida
            if 1 <= seleccion <= len(contenidoCarpeta):
                return contenidoCarpeta[seleccion - 1]  # Devuelve la ruta completa
            else:
                print("Por favor, introduzca un número válido:")
        except ValueError:
            print("Por favor, introduzca un número válido:")


## \brief Función para leer un archivo de ciudades en formato TSP.
#
#  Esta función abre un archivo seleccionado, lee sus contenidos y procesa las ciudades, almacenando sus datos en un objeto de la clase Mapa.
#
#  \param archivo La ruta completa del archivo que se va a leer.
#  \return Un objeto de la clase Mapa con las ciudades cargadas.
#
def leer_archivo(archivo):
    # Creamos un objeto Mapa
    miMapa = Mapa()
    # Bandera para indicar si hemos llegado a la sección de coordenadas
    seccionCoordenadas = False

    # Abrimos el archivo en modo lectura
    with open(archivo, "r") as archivo:
        for linea in archivo:
            linea = linea.strip()

            # Detectar cuando empieza la sección de coordenadas
            if linea == "NODE_COORD_SECTION":
                seccionCoordenadas = True
                continue

            # Detectar el final del archivo
            if linea == "EOF":
                break

            # Procesar las líneas de la cabecera antes de la sección de coordenadas
            if not seccionCoordenadas:
                if ":" in linea:
                    clave, valor = linea.split(":", 1)
                    clave = clave.strip().upper()
                    valor = valor.strip()

                    # Asignar los valores correspondientes a los atributos de Mapa
                    if clave == "NAME":
                        miMapa.nombre = valor
                    elif clave == "COMMENT":
                        miMapa.comentario = valor
                    elif clave == "TYPE":
                        miMapa.tipo = valor
                    elif clave == "DIMENSION":
                        miMapa.tam = int(valor)
                    elif clave == "EDGE_WEIGHT_TYPE":
                        miMapa.edge_type = valor
            else:
                # Procesar las coordenadas de las ciudades
                partes = linea.split()
                if len(partes) == 3:
                    id_nodo = int(partes[0])
                    x = float(partes[1])
                    y = float(partes[2])
                    # Crear una nueva instancia de Ciudad
                    ciudad = Ciudad(id_nodo, x, y)
                    # Añadir la ciudad al objeto Mapa
                    miMapa.ciudades[id_nodo] = ciudad
    print("Archivo procesado con éxito.")
    return miMapa


## \brief Función para imprimir los datos del mapa, incluyendo las ciudades y sus coordenadas.
#
#  \param miMapa Un objeto de la clase Mapa que contiene la información del mapa y las ciudades.
#
def imprimirMapa(miMapa):
    # Imprimir la cabecera del mapa
    print(f"Nombre: {miMapa.nombre}")
    print(f"Comentario: {miMapa.comentario}")
    print(f"Tipo: {miMapa.tipo}")
    print(f"Dimensión: {miMapa.tam}")
    print(f"Tipo de peso de arista: {miMapa.edge_type}")

    # Imprimir las coordenadas de las ciudades
    print("Coordenadas de las ciudades:")
    for ciudad in miMapa.ciudades.values():
        print(f"ID: {ciudad.id}, X: {ciudad.x}, Y: {ciudad.y}")


## \brief Función principal del programa.
#
#  Esta función coordina todo el proceso: desde listar archivos, permitir al usuario seleccionar uno, leer el archivo, mostrar el mapa, generar la matriz de distancias y ejecutar el algoritmo greedy.
#
def main():
    # Definir la ruta donde están los archivos TSP
    ruta_relativa = os.path.join('recursos', 'archivosTSP')
    archivos = buscarCarpeta(ruta_relativa)

    if archivos:
        # El usuario selecciona un archivo
        archivo_seleccionado = selecciona_archivo(archivos)
        # Leer el archivo y procesar las ciudades
        resultado = leer_archivo(archivo_seleccionado)

        # Preguntar si se deben mostrar los datos del mapa
        print('¿Desea mostrar los datos almacenados en la estructura?')
        mostrarResultados = input('Si/No: ')
        if mostrarResultados.lower() == 'si':
            imprimirMapa(resultado)
        else:
            print('Perfecto, no se imprimirán los datos almacenados en el mapa.')

        # Generar y mostrar la matriz de distancias si el usuario lo desea
        print('¿Desea imprimir la matriz de distancias?')
        mostrarMatriz = input('Si/No: ')
        matriz_d = resultado.generar_matriz_distancias()

        if mostrarMatriz.lower() == 'si':
            print('Mostrando la matriz de distancias:')
            for fila in matriz_d:
                print(fila)

        # Ejecutar el algoritmo greedy si el usuario lo desea
        print('¿Ejecuto el algoritmo greedy para saber la distancia mínima?')
        greedy = input('Si/No: ')
        if greedy.lower() == 'si':
            print('Mostrando distancia mínima:')
            minima = resultado.greedy()
            print(minima)
    else:
        print("No hay archivos seleccionados")


# Llamada a la función principal
main()
