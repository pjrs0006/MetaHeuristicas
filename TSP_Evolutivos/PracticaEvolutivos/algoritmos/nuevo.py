import numpy as np
import random
import logging
import time

from algoritmos.randomgreedy import randomgreedy


class nuevo:
    def __init__(self,  matriz_distancias, k, seed, tam, poblacionmax, porcentajealeatorio, Evmax, Tmax, kbest, kworst, procruce, promut, tipocruce):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam = tam
        self.poblacionmax=poblacionmax
        self.porcentajealeatorio= porcentajealeatorio
        self.Evmax=Evmax
        self.Tmax=Tmax
        self.kbest=kbest
        self.kworst = kworst
        self.probcruce=procruce
        self.probmut=promut
        self.tipocruce=tipocruce

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
        # Seleccionamos al azar 'k_best' individuos de la población para participar en el torneo
        participantes = random.sample(poblacion, k_best)
        # De los participantes, seleccionamos el individuo con el menor fitness (mejor aptitud)
        mejor = min(participantes, key=lambda ind: ind['fitness'])
        # Devolvemos el mejor individuo encontrado en el torneo
        return mejor

    def torneo_perdedores(self, poblacion, k_worst):
        # Se seleccionan k elementos para participar
        participantes = random.sample(poblacion, k_worst)
        # El ganador del torneo sera aquel que tenga el valor fitness mas alto
        peor = max(participantes, key=lambda ind: ind['fitness'])
        return peor

    def cruce_OX2(self, padre1, padre2):
        # obtenemos el tamaño de la permutacion
        size = len(padre1)
        # incializa el hijo como una lista vacia
        hijo = [None] * size
        # Genera una lista de indices aleatorios, en este caso la mitad de los indices posibles
        # Sorted se asegura que los indices esten ordenadoos de forma ascendente
        # Esta listaes de enteros que simbolizan la posicion que se copiara del padre al hijo
        indices = sorted(random.sample(range(size), size // 2))
        # Asigna los valores de 'padre1' a las posiciones correspondientes en 'hijo'
        # según los índices seleccionados aleatoriamente
        for idx in indices:
            hijo[idx] = padre1[idx]
        # Inicializa un puntero que ayudará a ubicar los valores restantes en 'hijo'
        puntero = 0
        # Itera a través de cada gen (elemento) en 'padre2'
        for gen in padre2:
            # Si el gen no está presente en 'hijo' (evitando duplicados)
            if gen not in hijo:
                # Busca la primera posición libre en 'hijo' (donde el valor es None)
                while hijo[puntero] is not None:
                    puntero += 1
                # Coloca el gen de 'padre2' en la posición libre
                hijo[puntero] = gen
        # Devuelve el hijo generado como una nueva permutación
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
        # Inicializamos la población inicial con individuos aleatorios
        poblacion = self.inicializar_poblacion()
        # Contador de evaluaciones igual al número de individuos en la población inicial
        evaluaciones = len(poblacion)
        # Registramos el tiempo de inicio para controlar el tiempo máximo de ejecución (Tmax)
        inicio = time.time()
        # Identificamos el mejor individuo inicial (con menor fitness)
        mejor_global = min(poblacion, key=lambda ind: ind['fitness'])

        # Bucle principal que se ejecuta hasta alcanzar Evmax evaluaciones o Tmax tiempo
        while evaluaciones < self.Evmax and (time.time() - inicio) < self.Tmax:
            # Selección: seleccionamos dos padres mediante torneo binario con 'kbest' participantes
            padre1 = self.torneo_binario(poblacion, self.kbest)
            padre2 = self.torneo_binario(poblacion, self.kbest)

            # Cruce: con probabilidad del 100% (siempre se realiza cruce en este caso)
            if random.random() < 1.0:
                # Decidimos aleatoriamente qué tipo de cruce utilizar (OX2 o MOC)
                if random.random() < 0.5:
                    # Realizamos cruce OX2 para generar los hijos
                    hijo1 = self.cruce_OX2(padre1['ruta'], padre2['ruta'])
                    hijo2 = self.cruce_OX2(padre2['ruta'], padre1['ruta'])
                else:
                    # Realizamos cruce MOC para generar los hijos
                    hijo1 = self.cruce_MOC(padre1['ruta'], padre2['ruta'])
                    hijo2 = self.cruce_MOC(padre2['ruta'], padre1['ruta'])
            else:
                # Si no se realiza cruce (aunque aquí siempre se realiza), copiamos los padres
                hijo1 = padre1['ruta'][:]
                hijo2 = padre2['ruta'][:]

            # Evaluamos los hijos calculando su fitness (distancia recorrida)
            fitness_hijo1 = self.dimedistancia(hijo1)
            fitness_hijo2 = self.dimedistancia(hijo2)
            # Actualizamos el contador de evaluaciones tras evaluar a los dos hijos
            evaluaciones += 2

            # Mutación: aplicamos mutación a los hijos con una cierta probabilidad
            if random.random() < self.probmut / 100:
                # Aplicamos la mutación 2-opt al primer hijo
                hijo1 = self.mutacion_2opt(hijo1)
                # Recalculamos su fitness después de la mutación
                fitness_hijo1 = self.dimedistancia(hijo1)
                # Incrementamos el contador de evaluaciones
                evaluaciones += 1
            if random.random() < self.probmut / 100:
                # Aplicamos la mutación 2-opt al segundo hijo
                hijo2 = self.mutacion_2opt(hijo2)
                # Recalculamos su fitness después de la mutación
                fitness_hijo2 = self.dimedistancia(hijo2)
                # Incrementamos el contador de evaluaciones
                evaluaciones += 1

            # Reemplazamiento: eliminamos dos individuos mediante torneo de perdedores con 'kworst' participantes
            for _ in range(2):
                # Seleccionamos el peor individuo entre 'kworst' participantes
                peor = self.torneo_perdedores(poblacion, self.kworst)
                # Eliminamos el peor individuo de la población
                poblacion.remove(peor)

            # Añadimos los hijos generados a la población
            poblacion.append({'ruta': hijo1, 'fitness': fitness_hijo1})
            poblacion.append({'ruta': hijo2, 'fitness': fitness_hijo2})

            # Actualizamos el mejor individuo global si alguno de los nuevos hijos es mejor
            posibles_mejores = [
                mejor_global,
                {'ruta': hijo1, 'fitness': fitness_hijo1},
                {'ruta': hijo2, 'fitness': fitness_hijo2}
            ]
            # Seleccionamos el individuo con el menor fitness como el nuevo mejor global
            mejor_global = min(posibles_mejores, key=lambda ind: ind['fitness'])

        # Al terminar el bucle, devolvemos el mejor individuo encontrado
        return mejor_global