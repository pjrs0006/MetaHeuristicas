import numpy as np
import random
import logging
import time

class evolutivoestacionario:
    def __init__(self, matriz_distancias, k, seed, tam, poblacionmax, porcentajealeatorio, Evmax, Tmax, kbest, kworst, procruce, promut):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam = tam
        self.poblacionmax = poblacionmax
        self.porcentajealeatorio = porcentajealeatorio
        self.Evmax = Evmax
        self.Tmax = Tmax
        self.kbest = kbest  # kBest=2 para torneo binario
        self.kworst = kworst  # kWorst=2 para torneo de perdedores
        self.probcruce = procruce # Probabilidad de cruce del 100%
        self.probmut = promut

        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        random.seed(seed)
        np.random.seed(seed)

    def randomGreedy(self):
        if self.k <= 0:
            logging.critical(f"\t\t\tEl parámetro k no es correcto: debe ser mayor que 0.")
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

    def dimedistancia(self, camino):
        camino_shifted = np.roll(camino, -1)
        distancias = self.matriz_distancias[camino, camino_shifted]
        return np.sum(distancias)

    def generar_individuo_aleatorio(self):
        ruta = list(range(self.tam))
        random.shuffle(ruta)
        return ruta

    def torneo_binario(self, poblacion, k_best):
        participantes = random.sample(poblacion, k_best)
        mejor = min(participantes, key=lambda ind: ind['fitness'])
        return mejor

    def torneo_perdedores(self, poblacion, k_worst):
        participantes = random.sample(poblacion, k_worst)
        peor = max(participantes, key=lambda ind: ind['fitness'])
        return peor

    def cruce_OX2(self, padre1, padre2):
        size = len(padre1)
        hijo = [None] * size
        indices = sorted(random.sample(range(size), size // 2))
        for idx in indices:
            hijo[idx] = padre1[idx]
        puntero = 0
        for gen in padre2:
            if gen not in hijo:
                while hijo[puntero] is not None:
                    puntero += 1
                hijo[puntero] = gen
        return hijo

    def cruce_MOC(self, padre1, padre2):
        size = len(padre1)
        hijo = [None] * size
        posicion = random.randint(0, size - 1)
        hijo[posicion] = padre1[posicion]
        gen = padre2[posicion]
        while gen not in hijo:
            indice = padre1.index(gen)
            hijo[indice] = gen
            gen = padre2[indice]
        for i in range(size):
            if hijo[i] is None:
                hijo[i] = padre2[i]
        return hijo

    def mutacion_2opt(self, individuo):
        a, b = random.sample(range(len(individuo)), 2)
        individuo[a], individuo[b] = individuo[b], individuo[a]
        return individuo

    # Inicialización
    def inicializar_poblacion(self):
        poblacion = []
        num_aleatorios = int((self.poblacionmax * self.porcentajealeatorio) / 100)
        numrestantes = self.poblacionmax - num_aleatorios

        # Generación de individuos aleatorios
        for _ in range(num_aleatorios):
            individuo = self.generar_individuo_aleatorio()
            fitness = self.dimedistancia(individuo)
            poblacion.append({'ruta': individuo, 'fitness': fitness})

        # Generación de individuos con randomGreedy
        for _ in range(numrestantes):
            individuo, fitness = self.randomGreedy()
            poblacion.append({'ruta': individuo, 'fitness': fitness})
        return poblacion

    # Algoritmo principal
    def ejecutar(self):
        poblacion = self.inicializar_poblacion()
        evaluaciones = len(poblacion)
        inicio = time.time()
        mejor_global = min(poblacion, key=lambda ind: ind['fitness'])

        while evaluaciones < self.Evmax and (time.time() - inicio) < self.Tmax:
            # Selección: seleccionar dos individuos mediante torneo binario con kBest=2
            padre1 = self.torneo_binario(poblacion, self.kbest)
            padre2 = self.torneo_binario(poblacion, self.kbest)

            # Cruce con probabilidad del 100%
            if random.random() < 1.0:
                if random.random() < 0.5:
                    hijo1 = self.cruce_OX2(padre1['ruta'], padre2['ruta'])
                    hijo2 = self.cruce_OX2(padre2['ruta'], padre1['ruta'])
                else:
                    hijo1 = self.cruce_MOC(padre1['ruta'], padre2['ruta'])
                    hijo2 = self.cruce_MOC(padre2['ruta'], padre1['ruta'])
            else:
                hijo1 = padre1['ruta'][:]
                hijo2 = padre2['ruta'][:]

            # Evaluar hijos
            fitness_hijo1 = self.dimedistancia(hijo1)
            fitness_hijo2 = self.dimedistancia(hijo2)
            evaluaciones += 2

            # Mutación
            if random.random() < self.probmut / 100:
                hijo1 = self.mutacion_2opt(hijo1)
                fitness_hijo1 = self.dimedistancia(hijo1)
                evaluaciones += 1
            if random.random() < self.probmut / 100:
                hijo2 = self.mutacion_2opt(hijo2)
                fitness_hijo2 = self.dimedistancia(hijo2)
                evaluaciones += 1

            # Reemplazamiento: reemplazar dos individuos mediante torneo de perdedores con kWorst=2
            for _ in range(2):
                peor = self.torneo_perdedores(poblacion, self.kworst)
                poblacion.remove(peor)

            # Añadir los hijos a la población
            poblacion.append({'ruta': hijo1, 'fitness': fitness_hijo1})
            poblacion.append({'ruta': hijo2, 'fitness': fitness_hijo2})

            # Actualizar mejor global si es necesario
            posibles_mejores = [mejor_global, {'ruta': hijo1, 'fitness': fitness_hijo1}, {'ruta': hijo2, 'fitness': fitness_hijo2}]
            mejor_global = min(posibles_mejores, key=lambda ind: ind['fitness'])

        return mejor_global

