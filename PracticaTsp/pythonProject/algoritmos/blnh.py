import numpy as np
import random
from concurrent.futures import ThreadPoolExecutor

class blnh:
    def __init__(self, matriz_distancias, k, seed, tam, iteraciones, tamentorno, dismentorno):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam = tam
        self.iteraciones = int(iteraciones)  # Número máximo de iteraciones
        self.tamentorno = float(tamentorno)  # Porcentaje inicial del entorno
        self.dismentorno = float(dismentorno)  # Porcentaje de disminución
        self.italgoritmo = 0  # Contador de iteraciones

        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        # Inicializar las semillas de random y numpy.random
        random.seed(seed)
        np.random.seed(seed)

    def randomGreedy(self):
        # Tu implementación actual permanece igual
        nc = self.tam
        marcaje = [False] * nc
        ruta = []
        suma_distancias = [(i, np.sum(self.matriz_distancias[i])) for i in range(nc)]
        suma_distancias.sort(key=lambda x: x[1])

        while len(ruta) < nc:
            disponibles = [ciudad for ciudad, _ in suma_distancias if not marcaje[ciudad]]
            if not disponibles:
                break
            k_actual = min(self.k, len(disponibles))
            ciudad_actual = random.choice(disponibles[:k_actual])
            ruta.append(ciudad_actual)
            marcaje[ciudad_actual] = True

        distancia_final = self.dimedistancia(ruta)
        return ruta, distancia_final

    def dimedistancia(self, camino):
        camino_shifted = np.roll(camino, -1)
        distancias = self.matriz_distancias[camino, camino_shifted]
        return np.sum(distancias)

    def two_opt_swap(self, camino, i, k):
        nuevo_camino = camino.copy()
        nuevo_camino[i:k+1] = camino[i:k+1][::-1]
        return nuevo_camino

    def delta_two_opt(self, ruta, i, j):
        n = len(ruta)
        ciudad_i_prev = ruta[i - 1]
        ciudad_i = ruta[i]
        ciudad_j = ruta[j]
        ciudad_j_next = ruta[(j + 1) % n]

        delta = 0
        delta -= self.matriz_distancias[ciudad_i_prev, ciudad_i]
        delta -= self.matriz_distancias[ciudad_j, ciudad_j_next]
        delta += self.matriz_distancias[ciudad_i_prev, ciudad_j]
        delta += self.matriz_distancias[ciudad_i, ciudad_j_next]
        return delta

    def generarymequedoconelmejor(self, ruta, distancia_actual, nv):
        """
        Genera nv vecinos usando el operador 2-opt y se queda con el mejor encontrado.

        :param ruta: arreglo de NumPy que representa el camino inicial.
        :param distancia_actual: distancia total de la ruta actual.
        :param nv: número de vecinos a generar.
        :return: mejor ruta encontrada, su distancia total y si hubo mejora.
        """

        # Inicializar la mejor ruta y su distancia
        mejor_ruta = ruta.copy()
        mejor_distancia = distancia_actual
        n = len(ruta)
        mejora = False

        # Generar índices i y j para nv vecinos
        indices_generados = []
        while len(indices_generados) < nv:
            i, j = np.random.choice(range(1, n - 1), 2, replace=False)
            i, j = min(i, j), max(i, j)
            if (j - i) <= 1:
                continue
            indices_generados.append((i, j))

        # Definir la función para evaluar un vecino
        def evaluar_vecino(args):
            i, j = args
            delta = self.delta_two_opt(ruta, i, j)
            return (i, j, delta)

        # Paralelizar la evaluación de vecinos
        with ThreadPoolExecutor() as executor:
            resultados = list(executor.map(evaluar_vecino, indices_generados))

        # Procesar los resultados
        for i, j, delta in resultados:
            if delta < 0:
                nueva_distancia = distancia_actual + delta
                if nueva_distancia < mejor_distancia:
                    mejor_ruta = self.two_opt_swap(ruta, i, j)
                    mejor_distancia = nueva_distancia
                    mejora = True

        return mejor_ruta, mejor_distancia, mejora

    def ejecutar(self):
        ruta_actual, distancia_actual = self.randomGreedy()
        iteracion_actual = 0  # Contador de iteraciones
        total_iteraciones = self.iteraciones
        tamano_entorno = int(total_iteraciones * self.tamentorno / 100)
        disminucion_entorno = self.dismentorno / 100
        intervalo_disminucion = int(total_iteraciones * 0.1)
        iteracion_proxima_disminucion = intervalo_disminucion
        mejora_global = True

        while iteracion_actual < total_iteraciones and mejora_global:
            mejora_global = False
            # Generar 'tamano_entorno' vecinos y quedarnos con el mejor
            ruta_nueva, distancia_nueva, mejora = self.generarymequedoconelmejor(
                ruta_actual, distancia_actual, tamano_entorno
            )
            # Si encontramos una mejor ruta, actualizamos
            if mejora and distancia_nueva < distancia_actual:
                ruta_actual = ruta_nueva
                distancia_actual = distancia_nueva
                mejora_global = True  # Hay mejora en esta iteración

            iteracion_actual += 1  # Incrementamos las iteraciones totales

            # Disminuir el tamaño del entorno si corresponde
            if iteracion_actual >= iteracion_proxima_disminucion:
                tamano_entorno = int(tamano_entorno - (tamano_entorno * disminucion_entorno))
                iteracion_proxima_disminucion += intervalo_disminucion

            # Si no hubo mejora, el algoritmo termina
            if not mejora_global:
                print("No se encontró mejora en los vecinos generados.")
                break

        return ruta_actual, distancia_actual
