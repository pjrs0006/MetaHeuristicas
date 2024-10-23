import numpy as np
import random

class busquedalocal:
    def __init__(self, matriz_distancias, k, seed, tam, iteraciones, tamentorno, dismentorno, itDismin):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam = tam
        self.iteraciones = int(iteraciones)  # Total de iteraciones exitosas
        self.tamentorno = float(tamentorno)  # Porcentaje inicial del entorno
        self.dismentorno = float(dismentorno)  # Porcentaje de disminución
        self.itDismin = float(itDismin)
        self.italgoritmo = 0  # Contador de iteraciones exitosas

        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        random.seed(seed)
        np.random.seed(seed)

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

    def dimedistancia(self, camino):
        camino_shifted = np.roll(camino, -1) # si hay la (123) se calcula la (231) y accediendo a la matriz se calculan sus distancias
        distancias = self.matriz_distancias[camino, camino_shifted] #genera un vector con las distancias obtenidas
        return np.sum(distancias)+ self.matriz_distancias[camino[-1], camino[0]] #np.sum suma las distancias de todos

    def two_opt_swap(self,camino, i, k):
        """
        Realiza un intercambio 2-opt entre las posiciones i y k en el camino.

        :param camino: arreglo (lista o numpy array) que representa el camino actual.
        :param i: índice inicial del segmento a invertir.
        :param k: índice final del segmento a invertir.
        :return: nuevo camino después del intercambio 2-opt.
        """
        nuevo_camino = camino.copy()
        nuevo_camino[i:k+1] = camino[i:k+1][::-1]
        return nuevo_camino

    def generarymequedoconelmejor(self, ruta, nv):
        """
        Genera nv vecinos usando el operador 2-opt y se queda con el mejor encontrado.

        :param ruta: arreglo de NumPy que representa el camino inicial.
        :param nv: número de vecinos a generar.
        :return: mejor ruta encontrada y su distancia total.
        """

        # Inicializar la mejor ruta y su distancia
        mejor_ruta = ruta.copy()
        mejor_distancia = self.dimedistancia(mejor_ruta)
        n = len(ruta)
        vecinos_generados = 0
        mejora=False

        while vecinos_generados < nv: #no sale del bucle hasta que no haga todos los vecinos
            # Generar índices i y j para el 2-opt, asegurando que i < j
            i, j = np.random.choice(range(1, n - 1), 2, replace=False) #range(1, n - 1) evita que se cambien la primera y ultima ciudad
            i, j = min(i, j), max(i, j) #para que funcione nuevo_camino[i:k+1] = camino[i:k+1][::-1]

            # Evitar casos donde i y j sean adyacentes o iguales
            if i == j or (j - i) <= 1:
                continue

            # Generar nuevo vecino aplicando el operador 2-opt
            #nuevo_ruta = self.two_opt_swap(mejor_ruta, i, j)

            '''El valor delta representa el cambio en la distancia total de la ruta cuando aplicamos un intercambio 2-opt entre las posiciones i y j.
            
            Si delta < 0: Significa que el intercambio reduce la distancia total de la ruta; es decir, hemos encontrado una ruta mejor (más corta).
            Si delta > 0: El intercambio aumenta la distancia total de la ruta; la nueva ruta es peor que la actual.
            Si delta == 0: No hay cambio en la distancia total; la ruta es igual en términos de longitud.'''

            # Calcular la distancia del nuevo vecino
            #nueva_distancia = self.dimedistancia(nuevo_ruta)
            nuevo_ruta,delta = self.delta_two_opt(mejor_ruta, i, j)
            vecinos_generados += 1
            # Si la distancia mejora, actualizar la mejor ruta y distancia
            if delta < 0:#mejor_distancia:
                mejor_ruta = nuevo_ruta
               # mejor_distancia = nueva_distancia
                mejor_distancia += delta
                mejora = True  # Se encontró una mejora

        return mejor_ruta, mejor_distancia,mejora

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
        # Realizar el intercambio 2-opt
        nuevo_ruta = ruta.copy()
        nuevo_ruta[i:j + 1] = ruta[i:j + 1][::-1]

        return nuevo_ruta, delta

    def ejecutar(self):

        ruta_actual, distancia_actual = self.randomGreedy()
        iteracion_actual = 0#contador de iteraciones
        total_iteraciones = self.iteraciones  # 5000
        tamano_entorno = int(total_iteraciones * self.tamentorno / 100)  # Tamaño inicial del entorno
        disminucion_entorno = self.dismentorno / 100  # Porcentaje de disminución por intervalo
        intervalo_disminucion = int(total_iteraciones * self.itDismin/100)  # Cada 10% del total de iteraciones
        iteracion_proxima_disminucion = intervalo_disminucion
        mejora_global = True  # Indica si hubo mejora en la última iteración

        while iteracion_actual < total_iteraciones and mejora_global:
            # Generar 'tamano_entorno' vecinos y quedarnos con el mejor
            ruta_nueva, distancia_nueva,mejora = self.generarymequedoconelmejor(ruta_actual, tamano_entorno)
            # Si encontramos una mejor ruta, actualizamos
            if mejora :
                ruta_actual = ruta_nueva
                distancia_actual = distancia_nueva
                mejora_global=True#hay mejora en esta iteracion
                iteracion_actual += 1  # Incrementamos las iteraciones exitosas
                #print(distancia_actual)
                #print(tamano_entorno)
                # Disminuir el tamaño del entorno si corresponde
                if iteracion_actual >= iteracion_proxima_disminucion:
                    tamano_entorno = int(tamano_entorno - (tamano_entorno * disminucion_entorno))
                    iteracion_proxima_disminucion += intervalo_disminucion

            else:
                #print("No se encontró mejora en los vecinos generados.")
                break
        return ruta_actual, distancia_actual