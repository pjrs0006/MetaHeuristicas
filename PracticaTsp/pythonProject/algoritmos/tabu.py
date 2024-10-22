import numpy as np
import random


class tabu:
    def __init__(self, matriz_distancias, k, seed, tam, iteraciones, tamentorno, dismentorno, porcentajel, tendencia_tabu):
        self.matriz_distancias = matriz_distancias
        self.k = k
        self.seed = seed
        self.tam = tam
        #He introducido casting para asegurar los tipos porque daba error
        self.iteraciones = int(iteraciones)
        self.tamentorno = float(tamentorno)
        self.dismentorno = float(dismentorno)
        self.porcentajel = float(porcentajel)  # Oscilación estratégica
        self.tenencia_tabu = int(tendencia_tabu)
        self.MCP = np.zeros((tam, tam), dtype=int)  # Memoria a corto plazo
        self.MLP = np.zeros((tam, tam), dtype=int)  # Memoria a largo plazo
        self.limiteEstancamiento = int(0.05 * iteraciones)  # 5% de iteraciones para considerar estancamiento
        self.contadorEstancamiento = 0  # Contador movimientos de empeoramiento

        if self.k <= 0:
            raise ValueError("El parámetro k no es correcto: debe ser mayor que 0.")
        random.seed(seed)
        np.random.seed(seed)

    def randomGreedy(self):
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

        distancia_final = self.calculaDistancia(ruta)
        return ruta, distancia_final

    #Calculamos la distancia total de una ruta proporcionando un camino
    def calculaDistancia(self, camino):
        camino_shifted = np.roll(camino, -1)
        distancias = self.matriz_distancias[camino, camino_shifted]
        return np.sum(distancias)+ self.matriz_distancias[camino[-1], camino[0]]
    #Generamos vecinos y nos quedamos con el mejor
    def generar_vecinos(self, ruta, nv):
        mejor_ruta = ruta.copy()
        mejor_distancia = self.calculaDistancia(mejor_ruta)
        n = len(ruta)
        mejora = False

        for _ in range(nv):
            i, j = sorted(random.sample(range(1, n - 1), 2))
            nuevo_ruta, delta = self.delta_two_opt(mejor_ruta, i, j)

            if delta < 0:
                mejor_ruta = nuevo_ruta
                mejor_distancia += delta
                mejora = True

        return mejor_ruta, mejor_distancia, mejora

    def delta_two_opt(self, ruta, i, j):
        """Calcula el delta de un movimiento 2-opt."""
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

        nuevo_ruta = ruta.copy()
        nuevo_ruta[i:j + 1] = ruta[i:j + 1][::-1]

        return nuevo_ruta, delta

    def actualizar_mcp(self):
        self.MCP[self.MCP > 0] -= 1

    def ejecutar(self):
        ruta_actual, distancia_actual = self.randomGreedy()
        mejor_global = ruta_actual.copy()
        mejor_distancia_global = distancia_actual

        iteracion_actual = 0
        tamano_entorno = int(self.iteraciones * self.tamentorno / 100)
        intervalo_disminucion = int(self.iteraciones * self.dismentorno / 100)

        while iteracion_actual < self.iteraciones:
            self.actualizar_mcp()
            ruta_nueva, distancia_nueva, mejora = self.generar_vecinos(ruta_actual, tamano_entorno)

            if mejora:
                ruta_actual = ruta_nueva
                distancia_actual = distancia_nueva
                if distancia_nueva < mejor_distancia_global:
                    mejor_global = ruta_nueva
                    mejor_distancia_global = distancia_nueva
                    self.contadorEstancamiento = 0  # Reinicia el contador de estancamiento
            else:
                self.contadorEstancamiento += 1

            if self.contadorEstancamiento >= self.limiteEstancamiento:
                ruta_actual = self.oscilacion_estrategica()
                self.contadorEstancamiento = 0

            iteracion_actual += 1
            if iteracion_actual % intervalo_disminucion == 0:
                tamano_entorno = max(1, int(tamano_entorno * 0.9))

        return mejor_global, mejor_distancia_global

    def oscilacion_estrategica(self):
        if random.random() < self.porcentajel:
            return self.diversificacion()
        else:
            return self.intensificacion()

    def diversificacion(self):
        return random.sample(range(self.tam), self.tam)

    def intensificacion(self):
        return np.argmax(self.MLP, axis=1)
