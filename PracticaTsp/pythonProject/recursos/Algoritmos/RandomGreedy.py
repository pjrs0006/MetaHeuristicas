import numpy as np
import random

class RandomGreedy:
    def __init__(self, matriz_distancias, k, seed):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed

        # Verificación de que k es mayor que 0
        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")

        # Cargamos la semilla en el random
        random.seed(seed)

    def ejecutar(self):
        nc = len(self.matriz_distancias)  # Número de ciudades
        suma = 0
        inicio = 0  # Empezamos desde la ciudad 0
        ruta = [inicio]  # Almacena el orden de las ciudades que visitamos

        # Creamos un vector de sumas de distancias
        suma_distancias = [(i, np.sum(self.matriz_distancias[i])) for i in range(nc)]
        suma_distancias.sort(key=lambda x: x[1])  # Ordenamos de menor a mayor

        while len(suma_distancias) > 0:
            # Seleccionamos de manera aleatoria entre los K primeros
            k_actual = min(self.k, len(suma_distancias))  # Aseguramos que k no exceda el tamaño de la lista
            filaSel = random.randint(0, k_actual - 1)
            ciudad_actual = suma_distancias[filaSel][0]

            # Añadimos la ciudad actual a la ruta
            ruta.append(ciudad_actual)

            # Actualizamos la suma de distancias
            suma += self.matriz_distancias[inicio][ciudad_actual]
            inicio = ciudad_actual

            # Eliminamos la tupla seleccionada
            suma_distancias.pop(filaSel)

        # Añadimos el regreso al punto de inicio
        suma += self.matriz_distancias[inicio][ruta[0]]
        ruta.append(ruta[0])

        return suma
