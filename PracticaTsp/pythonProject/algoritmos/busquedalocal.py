import numpy as np
import random


class busquedalocal:
    def __init__(self, matriz_distancias, k, seed, tam, iteraciones, tamentorno, dismentorno):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam = tam
        self.iteraciones = int(iteraciones)
        self.tamentorno = tamentorno
        self.dismentorno = int(dismentorno)
        self.italgoritmo = 0

        # Verificación de que k es mayor que 0
        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        # Cargamos la semilla en el random
        random.seed(seed)

    def dimedistancia(self, camino):
        if not camino:
            print("Camino vacio")
            return float('inf')  # Devolver infinita si el camino está vacío

        sumaDistancias = 0  # Para guardar el resultado
        for i in range(len(camino) - 1):
            ciudad_actual = camino[i]
            ciudad_siguiente = camino[i + 1]
            sumaDistancias += self.matriz_distancias[ciudad_actual][ciudad_siguiente]
        return sumaDistancias

    def evaluacion(self, distanciainicial, vecinos):
        minima = distanciainicial
        vecinoescogido = None

        for vecino in vecinos:
            distancia_vecino = self.dimedistancia(vecino)
            if distancia_vecino < minima:
                minima = distancia_vecino
                vecinoescogido = vecino
            else:
                print("Vecino Cabron")

        return vecinoescogido, minima, minima < distanciainicial

    def randomGreedy(self):
        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        nc = self.tam
        suma = 0
        marcaje = [False] * nc  # Lista para marcar las ciudades visitadas
        ruta = []
        suma_distancias = [(i, np.sum(self.matriz_distancias[i])) for i in range(nc)]
        suma_distancias.sort(key=lambda x: x[1])

        inicio = suma_distancias[0][0]
        while suma_distancias:
            if len(suma_distancias) < self.k:
                self.k = len(suma_distancias)

            filaSel = random.randint(0, self.k - 1)
            ciudad_actual = suma_distancias[filaSel][0]

            ruta.append(ciudad_actual)
            marcaje[ciudad_actual] = True
            suma += self.matriz_distancias[inicio][ciudad_actual]
            inicio = ciudad_actual
            suma_distancias.pop(filaSel)

        diatanciaFinal = self.dimedistancia(ruta)
        return ruta, diatanciaFinal

    def aplicar_2opt(self, ruta, i, k):
        nuevo_vecino = ruta[:i] + ruta[i:k + 1][::-1] + ruta[k + 1:]
        return nuevo_vecino

    def generar_vecinos(self, ruta, agenerar):
        vecinos = []
        for i in range(self.tam - 1):
            for k in range(i + 1, self.tam):
                if len(vecinos) >= agenerar:
                    return vecinos  # Retorna si se alcanza el límite
                nuevo_vecino = self.aplicar_2opt(ruta, i, k)
                if nuevo_vecino not in vecinos:  # Evitar duplicados
                    vecinos.append(nuevo_vecino)
        return vecinos

    def ejecutar(self):
        punto_inicio, distancia_inicial = self.randomGreedy()

        # Inicialización del entorno
        iteracion_actual = 0
        tamaño_entorno = int((self.tamentorno / 100) * self.iteraciones)

        while iteracion_actual < self.iteraciones:
            # Generar vecinos con el tamaño del entorno actual
            vecinos = self.generar_vecinos(punto_inicio, tamaño_entorno)
            # Evaluar vecinos
            vecino_mejorado, mejor_distancia, siesmejor = self.evaluacion(distancia_inicial, vecinos)

            # Si se encuentra un mejor vecino, actualizar la solución actual
            if siesmejor:
                punto_inicio = vecino_mejorado
                distancia_inicial = mejor_distancia
                iteracion_actual += 1  # Solo incrementa si se encontró una mejora

            # Ajustar el tamaño del entorno después de cada 500 iteraciones
            if (iteracion_actual + 1) % (self.iteraciones // self.dismentorno) == 0 and iteracion_actual != 0:
                tamaño_entorno = max(1, int(tamaño_entorno * self.dismentorno))  # Asegurar que no se reduzca a 0

            iteracion_actual += 1  # Incrementar el contador de iteraciones

        print("He encontrado un amigo")
        return punto_inicio, distancia_inicial  # Esto devolverá el mejor camino y su distancia
