import math
import sys
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

    import sys

    def prim(self):
        n = self.tam  # Número de nodos/ciudades
        T = []  # Lista para almacenar los bordes del MST
        mascer = [0] * n  # Nodo más cercano
        mindist = [0] * n  # Distancia mínima
        total_distancia = 0  # Variable para acumular la distancia total del MST

        # Inicialización: asumimos que la ciudad 0 está en el MST
        for i in range(1, n):
            mascer[i] = 0
            mindist[i] = [i][0]

        # Ciclo Greedy para construir el MST
        for _ in range(n - 1):
            # Encontrar el nodo con la distancia mínima
            min_dist = sys.maxsize
            k = -1
            for j in range(1, n):
                if 0 < mindist[j] < min_dist:
                    min_dist = mindist[j]
                    k = j

            # Añadir el borde al MST
            T.append((k, mascer[k]))

            # Sumar la distancia de este borde a la distancia total
            total_distancia += self.distancias[k][mascer[k]]

            # Marcar el nodo como añadido al MST
            mindist[k] = -1

            # Actualizar las distancias a los nodos restantes
            for j in range(1, n):
                if self.distancias[k][j] < mindist[j]:
                    mindist[j] = self.distancias[k][j]
                    mascer[j] = k

        return total_distancia

'''
    def greedy(self):
      nc = self.tam  # Número de ciudades
        suma = 0  # Acumula la distancia total recorrida
        marcaje = [0] * nc  # Lista para marcar qué ciudades ya han sido visitadas
        proxciudad = 0  # Comenzamos en la ciudad 0
        marcaje[0] = 1  # Marcamos la ciudad 0 como visitada

        for _ in range(nc - 1):  # Iteramos nc-1 veces (todas las ciudades menos la inicial)
            mejor = float('inf')  # Inicializamos la mejor distancia a infinito
            siguiente = -1  # Para almacenar la próxima ciudad a visitar

            # Buscamos la ciudad más cercana que no ha sido visitada
            for j in range(nc):
                if self.matriz_distancias[proxciudad][j] < mejor and marcaje[j] == 0:
                    mejor = self.matriz_distancias[proxciudad][j]
                    siguiente = j

            # Si encontramos una ciudad válida, actualizamos
            if siguiente != -1:
                suma += mejor  # Sumamos la distancia recorrida
                proxciudad = siguiente  # Actualizamos la ciudad actual
                marcaje[proxciudad] = 1  # Marcamos la nueva ciudad como visitada

        # Finalmente, volvemos a la ciudad de origen (ciudad 0)
        suma += self.matriz_distancias[proxciudad][0]

        return suma  # Retornamos la distancia total mínima estimada
'''
    # def greedy(self):
    #     nc = self.tam  # Número de ciudades
    #     tour = [0]  # Comenzamos en la ciudad 0
    #     marcaje = [0] * nc  # Lista para marcar qué ciudades ya han sido visitadas
    #     marcaje[0] = 1  # Marcamos la ciudad 0 como visitada
    #     proxciudad = 0  # Ciudad inicial
    #
    #     for _ in range(nc - 1):  # Visitamos nc-1 ciudades adicionales
    #         mejor = float('inf')
    #         siguiente = -1
    #         for j in range(nc):
    #             if self.matriz_distancias[proxciudad][j] < mejor and marcaje[j] == 0:
    #                 mejor = self.matriz_distancias[proxciudad][j]
    #                 siguiente = j
    #         proxciudad = siguiente
    #         tour.append(proxciudad)  # Añadimos la ciudad al recorrido
    #         marcaje[proxciudad] = 1  # Marcamos la ciudad como visitada
    #
    #     # Añadimos la vuelta al origen (ciudad 0)
    #     tour.append(0)
    #
    #     # Aplicamos la optimización 2-opt para mejorar la solución
    #     tour = self.aplicar_2opt(tour)
    #
    #     # Calculamos la distancia total del recorrido mejorado
    #     distancia_total = self.calcular_distancia_tour(tour)
    #     return distancia_total, tour
    #
    # def calcular_distancia_tour(self, tour):
    #     """Calcula la distancia total para un tour dado"""
    #     distancia = 0
    #     for i in range(len(tour) - 1):
    #         distancia += self.matriz_distancias[tour[i]][tour[i + 1]]
    #     return distancia
    #
    # def aplicar_2opt(self, tour):
    #     """Aplica el algoritmo 2-opt para mejorar el tour"""
    #     mejorado = True
    #     while mejorado:
    #         mejorado = False
    #         for i in range(1, len(tour) - 2):
    #             for j in range(i + 1, len(tour) - 1):
    #                 # Verificamos si el intercambio de dos aristas reduce la distancia
    #                 if self.intercambiar_si_mejora(tour, i, j):
    #                     tour[i:j + 1] = reversed(tour[i:j + 1])  # Revertimos la porción entre i y j
    #                     mejorado = True
    #     return tour
    #
    # def intercambiar_si_mejora(self, tour, i, j):
    #     """Verifica si al intercambiar dos aristas se obtiene una mejora"""
    #     a, b = tour[i - 1], tour[i]
    #     c, d = tour[j], tour[j + 1]
    #     # Verificamos si intercambiar mejora la distancia
    #     return (self.matriz_distancias[a][c] + self.matriz_distancias[b][d]) < \
    #         (self.matriz_distancias[a][b] + self.matriz_distancias[c][d])
