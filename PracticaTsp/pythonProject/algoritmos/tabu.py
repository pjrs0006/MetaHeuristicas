import numpy as np
import random


class tabu:
    def __init__(self, matriz_distancias, k, seed, tam, iteraciones, tamentorno, dismentorno,porcentajel):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam = tam
        self.iteraciones = int(iteraciones)  # Total de iteraciones exitosas
        self.tamentorno = float(tamentorno)  # Porcentaje inicial del entorno
        self.dismentorno = float(dismentorno)  # Porcentaje de disminución
        self.italgoritmo = 0  # Contador de iteraciones exitosas
        self.movimientos_empeoramiento = 0  # Contador de movimientos de empeoramiento consecutivos
        self.porcentajedeempeoramiento = porcentajel
        self.limite_empeoramiento = int(self.iteraciones * self.porcentajedeempeoramiento)  # Límite de movimientos de empeoramiento consecutivos

        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        random.seed(seed)

    # Funcion optimizada para eliminar el bucle
    def dimedistancia(self, camino):
        camino_shifted = np.roll(camino, -1)
        distancias = self.matriz_distancias[camino, camino_shifted]
        return np.sum(distancias)

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

    def ejecutar(self):
        punto_inicio, distancia_inicial = self.randomGreedy()
        mejor_momento_actual = punto_inicio[:]
        mejor_distancia_actual = distancia_inicial
        mejor_global = punto_inicio[:]
        mejor_distancia_global = distancia_inicial
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

            # Actualizar solución actual y distancia actual
            solucion_actual = vecino_mejorado
            distancia_actual = mejor_distancia
            if siesmejor:
                # Se encontró una mejora
                self.movimientos_empeoramiento = 0  # Reiniciar el contador de empeoramiento

                # Actualizar mejor momento actual si es mejor
                if distancia_actual < mejor_distancia_actual:
                    mejor_momento_actual = solucion_actual[:]
                    mejor_distancia_actual = distancia_actual

                iteracion_actual += 1  # Incrementar iteraciones exitosas

                # Actualizar mejor global si corresponde
                if distancia_actual < mejor_distancia_global:
                    mejor_global = solucion_actual[:]
                    mejor_distancia_global = distancia_actual

                # Reducir el tamaño del entorno cada 10% de las iteraciones exitosas
                if iteracion_actual >= proxima_disminucion:
                    tamaño_entorno = max(1, int(tamaño_entorno * (
                                1 - self.dismentorno / 100)))  # Reducir según dismentorno
                    proxima_disminucion += iteraciones_disminucion

            else:
                # No se encontró mejora en la solución actual
                self.movimientos_empeoramiento += 1

                # Verificar si se ha alcanzado el límite de movimientos de empeoramiento
                if self.movimientos_empeoramiento >= self.limite_empeoramiento:
                    print("El algoritmo se ha estancado tras varios movimientos de empeoramiento consecutivos.")
                    # Reiniciar con nueva solución
                    punto_inicio, distancia_inicial = self.randomGreedy()
                    solucion_actual = punto_inicio[:]
                    distancia_actual = distancia_inicial
                    mejor_momento_actual = punto_inicio[:]
                    mejor_distancia_actual = distancia_inicial
                    self.movimientos_empeoramiento = 0
                    # Continuar con el algoritmo
                    continue

            return mejor_global, mejor_distancia_global