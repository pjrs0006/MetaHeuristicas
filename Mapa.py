import math

import numpy as np


class Mapa:
    def __init__(self):
        self.ciudades = {}
        self.distancias = {}  # Diccionario para almacenar las distancias calculadas
        self.nombre = None
        self.comentario = None
        self.tipo = None
        self.tam = None
        self.edge_type = None

    def nueva_ciudad(self, nuevaciudad):
        self.ciudades[nuevaciudad.id] = nuevaciudad

    def calculadistancia(self, C1, C2):
        x1, y1 = C1.x, C1.y
        x2, y2 = C2.x, C2.y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def obtener_distancia(self, id1, id2):
        if id1 == id2:
            return 0  # La distancia a sí misma siempre es 0
        # Ordenamos los IDs para mantener simetría y evitar cálculos duplicados
        id_menor, id_mayor = sorted([id1, id2])
        if (id_menor, id_mayor) not in self.distancias:
            # Calculamos la distancia solo si no está en el diccionario
            distancia = self.calculadistancia(self.ciudades[id_menor], self.ciudades[id_mayor])
            self.distancias[(id_menor, id_mayor)] = distancia
        return self.distancias[(id_menor, id_mayor)]

    def generar_matriz_distancias(self):
        numCiudades = len(self.ciudades)
        # Crear una matriz de ceros utilizando numpy para mayor eficiencia
        self.matriz_distancias = np.zeros((numCiudades, numCiudades))

        for i, ciudad1 in enumerate(self.ciudades.values()):
            for j, ciudad2 in enumerate(self.ciudades.values()):
                self.matriz_distancias[i][j] = self.obtener_distancia(ciudad1.id, ciudad2.id)
        return self.matriz_distancias


    ##
    #  \brief Muestra una submatriz de distancias entre las ciudades.
    #
    #  \param filas Lista de índices de filas a mostrar. Si es None, se muestran todas las filas.
    #  \param columnas Lista de índices de columnas a mostrar. Si es None, se muestran todas las columnas.
    #
    #  Si no se especifican filas o columnas, se muestra la matriz completa de distancias.
    #
    def mostrar_matriz(self, filas=None, columnas=None):
        # Usar la lista completa si `filas` o `columnas` no se especifican
        # shape es un atributo del array que devuelve el tamaño del mismo
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
