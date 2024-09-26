import numpy as np
import random






class busquedalocal:
    def __init__(self, matriz_distancias, k, seed,tam):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam=tam
        #Variable para almacenar el camino mas corto
        self.mejorCamino=None
        #Variable para almacenar la distancia mas corta
        self.distanciaMinima=None
        # Verificación de que k es mayor que 0
        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        # Cargamos la semilla en el random
        random.seed(seed)

    def evaluacion(self, camino):
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
        return sumaDistancias + comienzo
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
                diatanciaFinal = self.evaluacion(ruta)

        return ruta, diatanciaFinal

    def ejecutar(self):
        miCamino = self.randomGreedy()[0]
        mejorRuta= self.evaluacion(miCamino)
        print("Estasi")
        print(mejorRuta)














