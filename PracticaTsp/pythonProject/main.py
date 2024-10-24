## \file main.py
#  \brief Este archivo contiene la lógica principal para procesar un conjunto de ciudades desde un archivo, generar la matriz de distancias y ejecutar un algoritmo greedy.

from Configurador import Configurador
from ejecucionesAutomaticas import EjecucionesAutomaticas


def main():
    # Crear una instancia del objeto Configurador
    configurador = Configurador()
    # Ejecutar el proceso de configuración, lectura de archivo y ejecución de algoritmo
    configurador.ejecutar()

main()

