#Realizamos las importaciones necesarias

import os

from numpy import select


# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Fernando')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# A partir de aqui comenzara el codigo para la lectura de ficheros:

# Para empezar comenzaremos obteniendo todos los nombres de los archivos que se encuentran en la carpeta:
def buscarCarpeta(carpeta):
    contenidoCarpeta = []
    for archivo in os.listdir(carpeta):
        # Crear la ruta completa
        ruta = os.path.join(carpeta, archivo)
        # Comprobar que es un archivo (no directorio)
        if os.path.isfile(ruta):
            contenidoCarpeta.append(ruta)
    return contenidoCarpeta

# Ahora mostramos al usuario la lista de archivos y le pedimos que seleccione uno
def selecciona_archivo(contenidoCarpeta):
    print("Seleccione el archivo que desea procesar:")
    # Mostrar solo los nombres de los archivos
    nombres_archivos = [os.path.basename(archivo) for archivo in contenidoCarpeta]
    for i, archivo in enumerate(nombres_archivos):
        print(f"    {i+1}................... {archivo}")

    while True:
        try:
            seleccion = int(input("Seleccione el número del archivo que desea procesar: "))
            if 1 <= seleccion <= len(contenidoCarpeta):
                return contenidoCarpeta[seleccion-1]  # Devolver la ruta completa
            else:
                print("Por favor, introduzca un número válido:")
        except ValueError:
            print("Por favor, introduzca un número válido:")
# Ahora tenemos que leer el archivo seleccionado por el usuario
def leer_archivo(archivo):
    print("Leyendo archivo")

# Definimos la función principal del programa
def main():
    # Ruta relativa desde el script
    ruta_relativa = os.path.join('recursos', 'practicaUnoDos')
    archivos = buscarCarpeta(ruta_relativa)
    if archivos:
        archivo_seleccionado = selecciona_archivo(archivos)
        leer_archivo(archivo_seleccionado)
    else:
        print("No hay archivos seleccionados")

# Llamamos a la funcion Main
main()
#Crearemos una lista donde tendremos la ubicacion de todos los archivos para cargarlos cuando los seleccionemos

#Seleccionamos el fichero que queremos leer

#Volcamos los datos del fichero a la clase