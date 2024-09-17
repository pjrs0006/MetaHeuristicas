# Realizamos los imports necesarios
import os
from Ciudad import Ciudad
from Mapa import Mapa


# Función para listar todos los archivos que contenga una carpeta
def buscarCarpeta(carpeta):
    #Creamos una lista para guardar los titulos de los ficheros
    contenidoCarpeta = []
    #Para cada archivo que encontremos en la carpeta metemos su titulo en la lista
    for archivo in os.listdir(carpeta):
        ruta = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta):
            contenidoCarpeta.append(ruta)
    return contenidoCarpeta


# Función para que el usuario seleccione un archivo
def selecciona_archivo(contenidoCarpeta):
    print("Listando los archivos TSP disponibles en el directorio:")
    nombres_archivos = [os.path.basename(archivo) for archivo in contenidoCarpeta]
    # Mostramos al usuario los archivos que tenemos en la lista
    for i, archivo in enumerate(nombres_archivos):
        print(f"    {i + 1}................... {archivo}")
    while True:
        try:
            # Pedimos al usuario que ingrese el numero correspondiente al fichero que desea procesar
            seleccion = int(input("Seleccione el número del archivo que desea procesar: "))
            if 1 <= seleccion <= len(contenidoCarpeta):
                return contenidoCarpeta[seleccion - 1]  # Devolver la ruta completa
            else:
                print("Por favor, introduzca un número válido:")
        except ValueError:
            print("Por favor, introduzca un número válido:")


# Función para leer el archivo seleccionado
def leer_archivo(archivo):
    # Creamos un objeto mapa con el constructor por defecto
    miMapa = Mapa()
    # El siguiente booleano servira para decirle al codigo cuando nos encontremos en la seccion de coordenadas
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

            # Procesar las líneas de la cabecera
            if not seccionCoordenadas:
                if ":" in linea:
                    clave, valor = linea.split(":", 1)
                    clave = clave.strip().upper()
                    valor = valor.strip()

                    # Asignar los valores correspondientes a la clase Mapa
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
                # Procesar las coordenadas después de "NODE_COORD_SECTION"
                partes = linea.split()
                if len(partes) == 3:
                    id_nodo = int(partes[0])
                    x = float(partes[1])
                    y = float(partes[2])
                    # Crear una instancia de la clase Ciudad
                    ciudad = Ciudad(id_nodo, x, y)
                    # Almacenar la instancia de 'Ciudad' en el diccionario 'ciudades'
                    miMapa.ciudades[id_nodo] = ciudad
    print("Archivo procesado con exito.")
    return miMapa
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

# Función principal del programa
def main():
    ruta_relativa = os.path.join('recursos', 'practicaUnoDos')
    archivos = buscarCarpeta(ruta_relativa)

    if archivos:
        archivo_seleccionado = selecciona_archivo(archivos)
        resultado = leer_archivo(archivo_seleccionado)
        print ('¿Desea mostrar los datos almacenados en la estructura?')
        mostrarResultados = input('Si/No: ')
        if mostrarResultados == 'Si' or mostrarResultados == 'si':
            imprimirMapa(resultado)
        else:
            print('Perfecto, no se imprimiran los datos almacenados en el mapa.')

        # Ahora rellenamos la matriz de distancias y la mostramos si el usuario lo desea:
        matriz_d = resultado.matrizDistancias()
        print('¿Desea imprimir la matriz de distancias?')
        mostrarMatriz = input('Si/No: ')
        if mostrarMatriz == 'Si' or mostrarMatriz == 'si':
            print('Mostrando la matriz de distancias:')
            for fila in matriz_d:
                print(fila)


    else:
        print("No hay archivos seleccionados")


# Llamada a la función principal
main()
