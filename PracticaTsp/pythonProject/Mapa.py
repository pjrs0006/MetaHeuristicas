## \file Mapa.py
#  \brief Este archivo contiene la clase Mapa, que gestiona un conjunto de ciudades y calcula las distancias entre ellas.
#
#  La clase Mapa permite añadir ciudades, generar una matriz de distancias entre todas las ciudades usando
#  las capacidades vectorizadas de numpy, y realizar cálculos como encontrar el camino más corto usando un algoritmo greedy.

import heapq
import math
import numpy as np
import random

from numpy import empty


## \class Mapa
#  \brief Clase que representa un mapa con ciudades y una matriz de distancias entre ellas.
#
#  Esta clase permite gestionar una colección de ciudades, calcular las distancias euclidianas entre ellas
#  y usar algoritmos como el Greedy para resolver problemas como el del viajero.
#
class Mapa:
    ## \brief Constructor de la clase Mapa.
    #
    #  Inicializa un mapa vacío que puede almacenar ciudades y generar una matriz de distancias.
    #
    def __init__(self):
        self.ciudades = {}  # Diccionario para almacenar las ciudades por su ID
        self.distancias = None  # Matriz de distancias calculada
        self.nombre = None  # Nombre del mapa
        self.comentario = None  # Comentario sobre el mapa
        self.tipo = None  # Tipo de mapa (TSP u otro)
        self.tam = None  # Número total de ciudades
        self.edge_type = None  # Tipo de cálculo de distancias (e.g., EUC_2D)

    ## \brief Añade una nueva ciudad al mapa.
    #
    #  \param nuevaciudad Objeto de la clase Ciudad que se va a añadir al mapa.
    #
    def nueva_ciudad(self, nuevaciudad):
        self.ciudades[nuevaciudad.id] = nuevaciudad

    ## \brief Genera la matriz de distancias entre todas las ciudades usando numpy.
    #
    #  La matriz de distancias se genera aprovechando las capacidades vectorizadas de numpy para
    #  calcular eficientemente las distancias euclidianas entre pares de ciudades.
    #
    #  \return Una matriz de distancias generada con numpy.
    #
    def generar_matriz_distancias(self):
        num_ciudades = len(self.ciudades)

        # Crear arrays numpy con las coordenadas x e y de las ciudades
        coords = np.array([(ciudad.x, ciudad.y) for ciudad in self.ciudades.values()])

        # Usar numpy para calcular la distancia euclidiana entre todos los pares de ciudades
        x_diff = np.subtract.outer(coords[:, 0], coords[:, 0])
        y_diff = np.subtract.outer(coords[:, 1], coords[:, 1])

        # Calcular la matriz de distancias
        self.matriz_distancias = np.sqrt(x_diff ** 2 + y_diff ** 2)
        self.distancias = self.matriz_distancias
        return self.matriz_distancias

    ## \brief Muestra una submatriz de distancias entre las ciudades.
    #
    #  \param filas Lista de índices de filas a mostrar. Si es None, se muestran todas las filas.
    #  \param columnas Lista de índices de columnas a mostrar. Si es None, se muestran todas las columnas.
    #
    def mostrar_matriz(self, filas=None, columnas=None):
        if self.matriz_distancias is None:
            print("Matriz de distancias no generada aún.")
            return

        filas = filas if filas is not None else range(self.matriz_distancias.shape[0])
        columnas = columnas if columnas is not None else range(self.matriz_distancias.shape[1])

        # Extraer y mostrar la submatriz
        submatriz = self.matriz_distancias[np.ix_(filas, columnas)]
        print(submatriz)

    ## \brief Algoritmo Greedy para resolver el problema del viajero.
    #
    #  Este método sigue un enfoque greedy para encontrar una solución aproximada
    #  al problema del viajero. Comienza en una ciudad y selecciona la ciudad más
    #  cercana que aún no ha sido visitada.
    #
    #  \return La suma total de distancias recorridas por la ruta greedy.
    #
    def greedy(self):
        nc = self.tam
        suma = 0
        marcaje = [0] * nc  # Lista para marcar las ciudades visitadas
        proxciudad = 0  # Empezamos desde la ciudad 0
        marcaje[0] = 1  # Marcamos la ciudad inicial como visitada
        for _ in range(nc - 1):
            mejor = float('inf')
            for j in range(nc):
                if self.matriz_distancias[proxciudad][j] < mejor and marcaje[j] == 0:
                    mejor = self.matriz_distancias[proxciudad][j]
                    siguiente = j
            suma += mejor
            proxciudad = siguiente
            marcaje[proxciudad] = 1
        suma += self.matriz_distancias[proxciudad][0]
        return suma

    # Algoritmo aleatorio:

    def randomGreedy(self, k, seed):
        # Cargamos la semilla en el random
        random.seed(seed)
        # En primer lugar tomaremos los datos que necesitaremos:
        nc = self.tam
        suma = 0
        '''marcaje = [False] * nc  # Lista para marcar las ciudades visitadas'''
        '''ruta = []''' # Almacena el orden de las ciudades que visitemos
        # Calcularemos el vector de sumas de distancias para cada ciudad
        suma_distancias = []
        for i in range(nc):
            suma_distancias.append((i, np.sum(self.matriz_distancias[i])))
        # Ordenamos el vector de menor a mayor
        suma_distancias.sort(key=lambda x: x[1])
        while suma_distancias is not empty():
            # Seleccionamos de manera aleatoria entre los K primeros uno de ellos
            filaSel = random.randint(0, k-1)
            ciudad_actual = suma_distancias[filaSel][0]
            # Ahora añadiremos la ciudad actual a la ruta que recorremos
            '''ruta.append(ciudad_actual)'''
            # Marcamos la ciudad en el vector de marcaje
            '''marcaje[ciudad_actual] = True'''
            # Eliminamos la tupla seleccionada y volvemos a lanzar
            suma += ciudad_actual
            suma_distancias.pop(filaSel)
        return suma








