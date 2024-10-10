import numpy as np
import random


class blh:
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

    # Funcion optimizada para eliminar el bucle, usando operaciones numpy vectorizadas
    def dimedistancia(self, camino):
        # Aseguramos que los índices de camino sean de tipo entero
        camino = np.array(camino, dtype=int)
        camino_shifted = np.roll(camino, -1)  # Desplazar el camino para calcular distancias entre pares
        return np.sum(self.matriz_distancias[camino, camino_shifted])  # Calcular la suma de las distancias

    # Método optimizado para la evaluación de vecinos
    def evaluacion(self, distanciainicial, vecinos):
        distancias = np.array([self.dimedistancia(vecino) for vecino in vecinos])
        mejor_vecino_idx = np.argmin(distancias)  # Encontrar el índice del mejor vecino
        mejor_distancia = distancias[mejor_vecino_idx]

        if mejor_distancia < distanciainicial:
            return vecinos[mejor_vecino_idx], mejor_distancia, True
        return None, distanciainicial, False

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

    # Optimización del algoritmo 2-opt, evitando cálculos innecesarios
    def aplicar_2opt(self, ruta, i, k):
        if i == 0 and k == len(ruta) - 1:
            return ruta
        nuevo_vecino = np.concatenate((ruta[:i], ruta[i:k + 1][::-1], ruta[k + 1:]))
        return nuevo_vecino

    # Generación eficiente de vecinos
    def generar_vecinos(self, ruta, num_vecinos):
        vecinos = []
        nc = len(ruta)
        indices = np.random.choice(np.arange(nc), (num_vecinos, 2), replace=False)
        for i, j in indices:
            vecino = self.aplicar_2opt(ruta, min(i, j), max(i, j))
            vecinos.append(vecino)
        return vecinos

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
            print(iteracion_actual)
            # Generar vecinos con el tamaño del entorno actual
            vecinos = self.generar_vecinos(punto_inicio, tamaño_entorno)

            # Evaluar vecinos
            vecino_mejorado, mejor_distancia, siesmejor = self.evaluacion(distancia_inicial, vecinos)
            indices = np.random.choice(np.arange(nc), (num_vecinos, 2), replace=False)
            for i, j in indices:
                vecino = self.aplicar_2opt(ruta, min(i, j), max(i, j))
                vecinos.append(vecino)
            return vecinos

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
                print("No se encontró mejora en los vecinos generados.")
                break

        return punto_inicio, distancia_inicial
