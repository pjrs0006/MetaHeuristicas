## \file main.py
#  \brief Este archivo contiene la lógica principal para procesar un conjunto de ciudades desde un archivo, generar la matriz de distancias y ejecutar un algoritmo greedy.

from Configurador import Configurador
from ejecucionesAutomaticas import EjecucionesAutomaticas


def main():
    print("¿Que modalidad desea ejecutar?")
    print("\t1",chr(10147), "Realizar todos los algoritmos automaticamente sobre el mismo fichero")
    print("\t2", chr(10147),"Realizar la ejecucion sobre el archivo indicado en el configurador con el algoritmo indicado en el configurador")
    print("\t0", chr(10147), "Cerrar programa")
    seleccion = int( input("Introduzca su eleccion:\t"))
    match seleccion:
        case 1:
            configurador=EjecucionesAutomaticas()
            configurador.ejecutar()
            input("Pulse ENTER para terminar la ejecucion")
        case 2:
            configurador = Configurador()
            configurador.ejecutar()
            input("Pulse ENTER para terminar la ejecucion")
        case 0:
            exit()

main()

