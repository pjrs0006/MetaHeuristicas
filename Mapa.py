import heapq
import math
import numpy as np


class Mapa:
    """
    Clase que representa un mapa con ciudades y una matriz de distancias entre ellas.

    Esta clase permite gestionar una colección de ciudades y calcular las distancias
    euclidianas entre ellas para generar una matriz de distancias.
    """

    def __init__(self):
        self.ciudades = {}  # Diccionario para almacenar las ciudades por su ID
        self.distancias = None  # Matriz de distancias calculada
        self.nombre = None
        self.comentario = None
        self.tipo = None
        self.tam = None
        self.edge_type = None

    def nueva_ciudad(self, nuevaciudad):
        """
        Añade una nueva ciudad al mapa.

        Args:
            nuevaciudad: Objeto de la clase Ciudad que se va a añadir al mapa.
        """
        self.ciudades[nuevaciudad.id] = nuevaciudad

    def generar_matriz_distancias(self):
        """
        Genera la matriz de distancias entre todas las ciudades de manera vectorizada usando numpy.

        La matriz de distancias se genera usando las capacidades vectorizadas de numpy
        para evitar cálculos redundantes y aprovechar la simetría de la matriz.

        Returns:
            Una matriz de distancias generada con numpy.
        """
        num_ciudades = len(self.ciudades)

        # Crear arrays numpy con las coordenadas x e y de las ciudades
        coords = np.array([(ciudad.x, ciudad.y) for ciudad in self.ciudades.values()])

        # Usar numpy para calcular la distancia euclidea entre todos los pares de ciudades
        x_diff = np.subtract.outer(coords[:, 0], coords[:, 0])
        y_diff = np.subtract.outer(coords[:, 1], coords[:, 1])

        # Calcular la matriz de distancias
        self.matriz_distancias = np.sqrt(x_diff ** 2 + y_diff ** 2)
        self.distancias = self.matriz_distancias
        return self.matriz_distancias

    def mostrar_matriz(self, filas=None, columnas=None):
        """
        Muestra una submatriz de distancias entre las ciudades.

        Args:
            filas: Lista de índices de filas a mostrar. Si es None, se muestran todas las filas.
            columnas: Lista de índices de columnas a mostrar. Si es None, se muestran todas las columnas.
        """
        if self.matriz_distancias is None:
            print("Matriz de distancias no generada aún.")
            return

        filas = filas if filas is not None else range(self.matriz_distancias.shape[0])
        columnas = columnas if columnas is not None else range(self.matriz_distancias.shape[1])

        # Extraer y mostrar la submatriz
        submatriz = self.matriz_distancias[np.ix_(filas, columnas)]
        print(submatriz)

    def greedy(self):
        nc=self.tam
        suma=0
        marcaje=[0]*nc
        proxciudad=0
        marcaje[0]=1
        for _ in range(nc-1):
            mejor = float('inf')
            for j in range(nc):
                if(self.matriz_distancias[proxciudad][j]<mejor and marcaje[j]==0):
                    mejor=self.matriz_distancias[proxciudad][j]
                    siguiente=j
            suma+=mejor
            proxciudad=siguiente
            marcaje[proxciudad]=1
        suma+=self.matriz_distancias[proxciudad][0]
        return suma

    def greedyDos(self):
        """
        Optimización del algoritmo Greedy usando un heap para acelerar la búsqueda
        de la ciudad más cercana no visitada.

        Returns:
            La suma total de distancias recorridas por la ruta greedy.
        """
        nc = self.tam  # Número de ciudades
        suma = 0
        marcaje = [False] * nc  # Lista para marcar las ciudades visitadas
        proxciudad = 0  # Empezamos desde la ciudad 0
        marcaje[0] = True  # Marcamos la ciudad inicial como visitada

        # Usamos un heap para almacenar las ciudades más cercanas
        heap = []

        # Añadir todas las distancias desde la ciudad inicial (0)
        for j in range(1, nc):
            heapq.heappush(heap, (self.matriz_distancias[proxciudad][j], j))

        # Iterar sobre las ciudades restantes
        for _ in range(nc - 1):
            # Extraer la ciudad no visitada más cercana del heap
            while True:
                mejor_distancia, siguiente = heapq.heappop(heap)
                if not marcaje[siguiente]:
                    break

            # Marcar la ciudad como visitada
            suma += mejor_distancia
            proxciudad = siguiente
            marcaje[proxciudad] = True

            # Añadir nuevas distancias desde la ciudad actual a las ciudades no visitadas
            for j in range(nc):
                if not marcaje[j]:
                    heapq.heappush(heap, (self.matriz_distancias[proxciudad][j], j))

        # Finalmente, sumar la distancia para volver a la ciudad inicial
        suma += self.matriz_distancias[proxciudad][0]
        return suma

