import numpy as np
import random
import logging
import time

from algoritmos.randomgreedy import randomgreedy


class evolutivogeneracional:
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
        camino_shifted = np.roll(camino, -1) # si hay la (123) se calcula la (231) y accediendo a la matriz se calculan sus distancias
        distancias = self.matriz_distancias[camino, camino_shifted] #genera un vector con las distancias obtenidas
        return np.sum(distancias)+ self.matriz_distancias[camino[-1], camino[0]] #np.sum suma las distancias de todos


    def generar_individuo_aleatorio(self):
        ruta = list(range(self.tam))
        random.shuffle(ruta)
        return ruta

    def torneo_ganadores(self, poblacion, k_best):
        #Lista que contiene los mejores
        ganadores = []
        for _ in range(len(poblacion)):
            #Seleccionamos K participantes aleatoriamente de la poblacion
            participantes = random.sample(poblacion, k_best)
            #Cogemos el que tenga el menor numero en el campo fitness
            mejor = min(participantes, key=lambda ind: ind['fitness'])
            #Añadimos el ganador a la lista de ganadores
            ganadores.append(mejor)
        return ganadores

    def torneo_perdedores(self,poblacion, k_worst):
        #Se seleccionan k elementos para participar
        participantes = random.sample(poblacion, k_worst)
        #El ganador del torneo sera aquel que tenga el valor fitness mas alto
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

    def cruce_MOC(self,padre1, padre2):
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

    def mutacion_2opt(self,individuo):
        a, b = random.sample(range(len(individuo)), 2)
        individuo[a], individuo[b] = individuo[b], individuo[a]
        return individuo

    # Inicialización
    def inicializar_poblacion(self):
        poblacion = []
        num_aleatorios = int((self.poblacionmax * self.porcentajealeatorio)/100)
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
        #Introduciremos un contador de tiempo para establecer la condicion de parada si se llega a Tmax.
        inicio = time.time()
        mejor_global = min(poblacion, key=lambda ind: ind['fitness'])
        while evaluaciones < self.Evmax and (time.time() - inicio) < self.Tmax:
            # Selección: Lista con los ganadores del torneo (Menor Fitness)
            padres = self.torneo_ganadores(poblacion, self.kbest)
            # Cruce: Lista de descendientes que contendra la siguiente generacion en estado base
            descendientes = []
            for i in range(0, len(padres), 2):
                padre1 = padres[i]['ruta']
                # Al seleccionar el segundo padre usamos el operador modulo de manera que permita el cruce circular
                padre2 = padres[(i + 1) % len(padres)]['ruta']
                # Decidimos aleatoriamente si se reralizara el cruce o sera copia de los padres
                # Si el random generado se menor que la probabilidad se producira el cruce
                if random.random() < self.probcruce/100:
                    # Si este parametro es 0 se realizara un tipo de cruce y si es otro valor sera otro
                    if self.tipocruce==0:
                        hijo1 = self.cruce_OX2(padre1, padre2)
                        hijo2 = self.cruce_OX2(padre2, padre1)
                    else:
                        hijo1 = self.cruce_MOC(padre1, padre2)
                        hijo2 = self.cruce_MOC(padre2, padre1)
                else:
                    # Si el resultado del random hace que no se realice cruce se copian directamente los padres:
                    hijo1 = padre1[:]
                    hijo2 = padre2[:]
                # Añadimos los dos hijos generados a nuestra lista de descendientes
                descendientes.append({'ruta': hijo1, 'fitness': self.dimedistancia(hijo1)})
                descendientes.append({'ruta': hijo2, 'fitness': self.dimedistancia(hijo2)})
                evaluaciones += 2
            # Mutación: Iteramos sobre cada individuo de los descendientes
            for individuo in descendientes:
                # Mediante una probabilidad aleatoria decidimos si se produce la mutacion o no:
                if random.random() < self.probmut/100:
                    # Si se produce la mutacion, aplicamos un 2-opt
                    individuo['ruta'] = self.mutacion_2opt(individuo['ruta'])
                    individuo['fitness'] = self.dimedistancia(individuo['ruta'])
                    evaluaciones += 1
            # Reemplazamiento: Reemplazamos totalmente la generacion anterior por la nueva
            poblacion_nueva = descendientes
            # Elitismo:
            # Seleccionamos el individuo con menor distancia (mejor fitness)
            mejor_nuevo = min(poblacion_nueva, key=lambda ind: ind['fitness'])
            # En caso de que el nuevo mejor sea peor que el mejor global, realizamos un torneo de perdedores
            if mejor_nuevo['fitness'] > mejor_global['fitness']:
                peor = self.torneo_perdedores(poblacion_nueva, self.kworst)
                # Para asegurar que las soluciones no pierdan calidad, preservaremos el elemento mejor global
                # Para preservar este elemento sustituimos el peor elemento actual por el individuo mejor global
                poblacion_nueva.remove(peor)
                poblacion_nueva.append(mejor_global)
            else:
                # Si no se da el caso anterior sustituiremos el mejor global por el nuevo mejor
                mejor_global = mejor_nuevo
            # Realizamos finalmente la siustitucion, dando paso a una nueva generacion
            poblacion = poblacion_nueva
        # Cuando ya se cumplen las condiciones de parada devolvemos el mejor individuo obtenido
        return mejor_global

    '''# Ejecución del algoritmo
    mejor_solucion = ejecutar()
    print("Mejor ruta encontrada:", mejor_solucion['ruta'])
    print("Costo de la ruta:", mejor_solucion['fitness'])'''