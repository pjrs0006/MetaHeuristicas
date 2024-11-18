import numpy as np
import random
import logging
import time

from algoritmos.randomgreedy import randomgreedy


class evolutivogeneracional:
    def __init__(self,  matriz_distancias, k, seed, tam, poblacionmax, porcentajealeatorio, Evmax, Tmax, kbest, kworst, procruce, promut, tipocruce, elite):
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
        self.elite=elite

        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        random.seed(seed)
        np.random.seed(seed)

    def randomGreedy(self):
        if self.k <= 0:
            logging.info(f"\t\t\tEl parámetro k no es correcto: debe ser mayor que 0.")
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

    def torneo_perdedores(self, poblacion, k_worst):
        # Inicializar una lista para los perdedores
        perdedores = []
        for _ in range(self.elite):
            # Seleccionar k participantes aleatorios de la población
            participantes = random.sample(poblacion, k_worst)
            # Escoger al peor de los participantes (mayor fitness)
            peor = max(participantes, key=lambda ind: ind['fitness'])
            # Añadir el peor a la lista de perdedores
            perdedores.append(peor)
        return perdedores

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

    # def mutacion_2opt(self,individuo):
    #     a, b = random.sample(range(len(individuo)), 2)
    #     individuo[a], individuo[b] = individuo[b], individuo[a]
    #     return individuo

    def mutacion_2opt(self, individuo):
        a, b = sorted(random.sample(range(len(individuo)), 2))
        individuo[a:b + 1] = reversed(individuo[a:b + 1])
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
        # Inicializar la población
        poblacion = self.inicializar_poblacion()
        evaluaciones = len(poblacion)
        inicio = time.time()
        logging.info(f'\t\t\tpoblacion inicial: {poblacion}')
        # Seleccionar los mejores individuos iniciales como élite
        mejor_global = sorted(poblacion, key=lambda ind: ind['fitness'])[:self.elite]
        logging.info(f'\t\t\telite(s): {mejor_global}')
        contador=0
        while evaluaciones < self.Evmax and (time.time() - inicio) < self.Tmax:
            # Selección: Elegir padres mediante torneo
            padres = self.torneo_ganadores(poblacion, self.kbest)
            descendientes = []
            if contador == 0:
                logging.info(f'\t\t\tPadres: {padres}')
            # Cruce: Generar descendientes a partir de los padres seleccionados
            for i in range(0, len(padres), 2):
                padre1 = padres[i]['ruta']
                padre2 = padres[(i + 1) % len(padres)]['ruta']

                if random.random() < self.probcruce / 100:
                    if self.tipocruce == 0:
                        hijo1 = self.cruce_OX2(padre1, padre2)
                        hijo2 = self.cruce_OX2(padre2, padre1)
                    else:
                        hijo1 = self.cruce_MOC(padre1, padre2)
                        hijo2 = self.cruce_MOC(padre2, padre1)
                else:
                    hijo1 = padre1[:]
                    hijo2 = padre2[:]

                descendientes.append({'ruta': hijo1, 'fitness': self.dimedistancia(hijo1)})
                descendientes.append({'ruta': hijo2, 'fitness': self.dimedistancia(hijo2)})
                evaluaciones += 2
            if contador == 0:
                logging.info(f'\t\t\thijos: {descendientes}')
            # Mutación: Aplicar mutaciones a los descendientes
            for individuo in descendientes:
                if random.random() < self.probmut / 100:
                    individuo['ruta'] = self.mutacion_2opt(individuo['ruta'])
                    individuo['fitness'] = self.dimedistancia(individuo['ruta'])
                    evaluaciones += 1

            # Reemplazar la población actual con los descendientes
            poblacion_nueva = descendientes
            # Seleccionar los mejores individuos de la nueva población como élite
            elite_individuos = sorted(poblacion_nueva, key=lambda ind: ind['fitness'])[:self.elite]

            logging.info(f'\t\t\tGeneracion: {contador+1}')
            for i in range(self.elite):
                logging.info(f'\t\t\t\tElite{i}: {elite_individuos[i]}\n') #pasiempre
            # Comparar el peor nuevo élite con el peor de los élites globales
            if elite_individuos[-1]['fitness'] > max(mejor_global, key=lambda ind: ind['fitness'])['fitness']:
                if contador == 0:
                    logging.info(f'\t\t\tel peor de los elites de la nueva generacion es peor que el elite de la antigua->se añaden el/los elite(s) de la generacion pasada')
                # Seleccionar los peores individuos en la nueva población
                peores_individuos = self.torneo_perdedores(poblacion_nueva, self.kworst)
                # Reemplazar los peores individuos con los mejores élites globales
                for peor, mejor_elite in zip(peores_individuos, mejor_global):
                    for i, individuo in enumerate(poblacion_nueva):
                        if individuo['ruta'] == peor['ruta'] and float(individuo['fitness']) == float(peor['fitness']):
                            poblacion_nueva[i] = mejor_elite
                            break
            else:
                # Actualizar el conjunto global de élites
                mejor_global = elite_individuos

            # Actualizar la población con la nueva generación
            poblacion = poblacion_nueva
            contador+=1
        if contador == 0:
            logging.info(f'\t\t\tNueva poblacion: {poblacion}')
        # Devolver el mejor individuo encontrado en todas las generaciones
        return min(mejor_global, key=lambda ind: ind['fitness'])

    '''# Ejecución del algoritmo
    mejor_solucion = ejecutar()
    print("Mejor ruta encontrada:", mejor_solucion['ruta'])
    print("Costo de la ruta:", mejor_solucion['fitness'])'''