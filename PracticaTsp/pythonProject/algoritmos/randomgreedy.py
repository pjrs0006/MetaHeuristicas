import numpy as np
import random

class randomgreedy:
    def __init__(self, matriz_distancias, k, seed,tam):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam=tam
        # Verificación de que k es mayor que 0
        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        # Cargamos la semilla en el random
        random.seed(seed)

    def ejecutar(self):
        # Verificación de que k es mayor que 0
        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")
        # En primer lugar tomaremos los datos que necesitaremos:
        nc = self.tam
        suma = 0
        '''marcaje = [False] * nc  # Lista para marcar las ciudades visitadas'''
        '''ruta = []'''  # Almacena el orden de las ciudades que visitemos
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
                '''ruta.append(ciudad_actual)'''
                # Marcamos la ciudad en el vector de marcaje
                '''marcaje[ciudad_actual] = True'''
                # Eliminamos la tupla seleccionada y volvemos a lanzar
                suma += self.matriz_distancias[inicio][ciudad_actual]
                inicio = ciudad_actual
                suma_distancias.pop(filaSel)
        return suma + self.matriz_distancias[inicio][0]
