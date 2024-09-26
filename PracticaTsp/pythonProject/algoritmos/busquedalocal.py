import numpy as np
import random

class busquedalocal:
    def __init__(self, matriz_distancias, k, seed,tam,it,tamentorno,dismentorno):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam=tam
        self.iteraciones= it
        self.tamentorno = tamentorno
        self.dismentorno = dismentorno
        #iteraciones que haga el algoritmo
        self.italgoritmo=0
        # Verificación de que k es mayor que 0
        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        # Cargamos la semilla en el random
        random.seed(seed)

    def dimedistancia(self,camino):
        # Verificamos que el camino esta completado
        if not camino:
            print("Camino vacio")
            return False
        # Recorremos cada ciudad y en la matriz de distancias vamos sumando
        sumaDistancias = 0  # Para guardar el resultado
        comienzo = camino[0]
        for i in range(len(camino) - 1):
            # Ahora en las siguientes variables guardamos la ciudad en la que estamos y la siguiente
            ciudad_actual = camino[i]
            ciudad_siguiente = camino[i + 1]
            # Calculamos la distancia entre los dos
            sumaDistancias += self.matriz_distancias[ciudad_actual][ciudad_siguiente]
        return sumaDistancias

    def evaluacion(self,distanciainicial,vecinos):
        minima=distanciainicial
        for i in range(len(vecinos)):
            if self.dimedistancia(vecinos[i]) < minima:
                minima = self.dimedistancia(vecinos[i])
                vecinoescogido=vecinos[i]
        if minima<distanciainicial:
            return vecinoescogido,minima,True
        else:
            return vecinoescogido,minima,False


    # Esta función nos generara el primer entorno de manera aleatoria que actuara como punto de partida
    def randomGreedy(self):
        # Verificación de que k es mayor que 0
        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")
        # En primer lugar tomaremos los datos que necesitaremos:
        nc = self.tam
        suma = 0
        marcaje = [False] * nc  # Lista para marcar las ciudades visitadas
        ruta = []  # Almacena el orden de las ciudades que visitemos
        # Calcularemos el vector de sumas de distancias para cada ciudad
        suma_distancias = []

        for i in range(nc):
            suma_distancias.append((i, np.sum(self.matriz_distancias[i])))
        # Ordenamos el vector de menor a mayor
        suma_distancias.sort(key=lambda x: x[1])
        inicio = suma_distancias[0][0]
        while len(suma_distancias) > 0:
            # Seleccionamos de manera aleatoria entre los K primeros uno de ellos
            if len(suma_distancias) < self.k:
                self.k = len(suma_distancias)

            if self.k > 0:
                filaSel = random.randint(0, self.k - 1)
                # print(filaSel)

                ciudad_actual = suma_distancias[filaSel][0]

                # Ahora añadiremos la ciudad actual a la ruta que recorremos
                ruta.append(ciudad_actual)
                # Marcamos la ciudad en el vector de marcaje
                marcaje[ciudad_actual] = True
                # Eliminamos la tupla seleccionada y volvemos a lanzar
                suma += self.matriz_distancias[inicio][ciudad_actual]
                inicio = ciudad_actual
                suma_distancias.pop(filaSel)
                diatanciaFinal = self.dimedistancia(ruta)

        return ruta, diatanciaFinal

    #metodo para aplicar operador 2_opt
    def aplicar_2opt(ruta, i, k):
        nuevo_vecino = ruta[:i] + ruta[i:k + 1][::-1] + ruta[k + 1:]
        return nuevo_vecino

    #metodo que genera los vecinos a analizar
    def generar_vecinos(self,ruta,agenerar):
        vecinos=[]
        for i in range(self.tam - 1):
            for k in range(i + 1, self.tam):
                if len(vecinos) >= agenerar:
                    return vecinos  # Retorna si se alcanza el límite
                nuevo_vecino = self.aplicar_2opt(ruta, i, k)
                if nuevo_vecino not in vecinos:  # Evitar duplicados
                    vecinos.append(nuevo_vecino)
        return vecinos

    def ejecutar(self):
        punto_inicio = self.randomGreedy()[0]
        distancia_inicial = self.randomGreedy()[1]

        # Inicialización del entorno
        iteracion_actual = 0
        tamaño_entorno = int((self.tamentorno / 100) * self.iteraciones)

        while iteracion_actual < self.iteraciones:
            # Generar vecinos con el tamaño del entorno actual
            vecinos = self.generar_vecinos(punto_inicio, tamaño_entorno)

            # Evaluar vecinos
            vecino_mejorado, mejor_distancia, mejorado = self.evaluacion(distancia_inicial, vecinos)

            # Si se encuentra un mejor vecino, actualizar la solución actual
            if mejorado:
                punto_inicio = vecino_mejorado
                distancia_inicial = mejor_distancia
                self.italgoritmo += 1  # Solo incrementa si se encontró una mejora

            # Ajustar el tamaño del entorno después de cada 500 iteraciones
            if (iteracion_actual + 1) % (self.iteraciones // self.dismentorno) == 0 and iteracion_actual != 0::
                tamaño_entorno = int(tamaño_entorno * self.dismentorno)  # Reducir el tamaño en un 10%

            iteracion_actual += 1  # Incrementar el contador de iteraciones
    return punto_inicio, distancia_inicial  # Esto devolverá el mejor camino y su distancia















