import numpy as np
import random


class busquedalocal:
    def __init__(self, matriz_distancias, k, seed, tam, iteraciones, tamentorno, dismentorno):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam = tam
        self.iteraciones = int(iteraciones)  # Total de iteraciones exitosas
        self.tamentorno = float(tamentorno)  # Porcentaje inicial del entorno
        self.dismentorno = float(dismentorno)  # Porcentaje de disminución
        self.italgoritmo = 0  # Contador de iteraciones exitosas

        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        random.seed(seed)

    #Funcion optimizada para eliminar el bucle
    def dimedistancia(self, camino):
        camino_shifted = np.roll(camino, -1)
        distancias = self.matriz_distancias[camino, camino_shifted]
        return np.sum(distancias)

    # def dimedistancia(self, camino):
    #     if not camino:
    #         print("Camino vacío")
    #         return float('inf')
    #
    #     sumaDistancias = 0
    #     for i in range(len(camino) - 1):
    #         ciudad_actual = camino[i]
    #         ciudad_siguiente = camino[i + 1]
    #         sumaDistancias += self.matriz_distancias[ciudad_actual][ciudad_siguiente]
    #     # Añadir distancia de regreso al inicio para cerrar el ciclo
    #     sumaDistancias += self.matriz_distancias[camino[-1]][camino[0]]
    #     return sumaDistancias

    def evaluacion(self, distanciainicial, vecinos):
        minima = distanciainicial
        vecinoescogido = None
        for vecino in vecinos:
            distancia_vecino = self.dimedistancia(vecino)
            if distancia_vecino < minima:
                minima = distancia_vecino
                vecinoescogido = vecino
        return vecinoescogido, minima, vecinoescogido is not None

    def randomGreedy(self):
        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

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

    def aplicar_2opt(self, ruta, i, k):
        # Manejo especial si i es 0 y k es la última ciudad
        if i == 0 and k == len(ruta) - 1:
            return ruta  # No hacemos nada
        nuevo_vecino = ruta[:i] + ruta[i:k + 1][::-1] + ruta[k + 1:]
        return nuevo_vecino


    # Funcion Optimizada

    def generar_vecinos(self, ruta, num_vecinos):
        vecinos = []
        for _ in range(num_vecinos):
            i, j = sorted(random.sample(range(len(ruta)), 2))
            if i != j:
                vecino = self.aplicar_2opt(ruta, i, j)
                vecinos.append(vecino)

        return vecinos

    # def generar_vecinos(self, ruta, num_vecinos):
    #     vecinos = set()
    #     intentos = 0
    #     max_intentos = num_vecinos * 10  # Evitar bucles infinitos
    #
    #     while len(vecinos) < num_vecinos and intentos < max_intentos:
    #         i, j = sorted(random.sample(range(len(ruta)), 2))
    #         # Evitar intercambios que no modifiquen la ruta
    #         if (i == 0 and j == len(ruta) - 1) or i == j:
    #             intentos += 1
    #             continue
    #         nuevo_vecino = tuple(self.aplicar_2opt(ruta, i, j))
    #         vecinos.add(nuevo_vecino)
    #         intentos += 1
    #
    #     return [list(vecino) for vecino in vecinos]

    def ejecutar(self):
        punto_inicio, distancia_inicial = self.randomGreedy()
        iteracion_actual = 0  # Iteraciones exitosas
        total_iteraciones = self.iteraciones

        # Tamaño inicial del entorno dinámico
        tamaño_entorno = int(total_iteraciones * self.tamentorno / 100)

        # Cada 10% de iteraciones exitosas, reduciremos el tamaño del entorno
        iteraciones_disminucion = int(total_iteraciones * 0.10)
        proxima_disminucion = iteraciones_disminucion

        while iteracion_actual < total_iteraciones:
            # Generar vecinos con el tamaño del entorno actual
            vecinos = self.generar_vecinos(punto_inicio, tamaño_entorno)

            # Evaluar vecinos
            vecino_mejorado, mejor_distancia, siesmejor = self.evaluacion(distancia_inicial, vecinos)

            # Si se encuentra un mejor vecino, actualizar la solución actual
            if siesmejor:
                punto_inicio = vecino_mejorado
                distancia_inicial = mejor_distancia
                iteracion_actual += 1  # Incrementar solo si se encontró una mejora
                self.italgoritmo += 1

                # Reducir el tamaño del entorno cada 10% de las iteraciones exitosas
                if iteracion_actual == proxima_disminucion:
                    tamaño_entorno = max(1, int(tamaño_entorno * 0.90))  # Reducir en un 10%
                    proxima_disminucion += iteraciones_disminucion
            else:
                # No se encontró mejora; continuamos sin incrementar el contador
                print("No se encontró mejora en los vecinos generados.")

                # Podemos decidir si queremos terminar el algoritmo aquí o continuar
                # Si no se encuentran mejoras después de cierto número de intentos, podemos romper el bucle
                break  # En este caso, terminamos el algoritmo

        return punto_inicio, distancia_inicial
