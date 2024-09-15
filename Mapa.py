from Ciudad import Ciudad
import numpy as np
import math
class Mapa:
    def __init__(self):
        self.ciudades={}
        self.matriz_distancias=np.inf

    def nueva_ciudad(self,nuevaciudad):
        self.ciudades[nuevaciudad.id]=nuevaciudad

    def calculadistancia(self,C1,C2):
        x1,y1=C1.x,C1.y
        x2,y2=C2.x,C2.y
        return math.sqrt((x2-x1)**2+(y2-y1)**2)


    def mostrar_matriz(self, filas=None, columnas=None):
        # Usar la lista completa si `filas` o `columnas` no se especifican
        #shape es un atriubuto del array que devuelve el tamaño del mismo
        filas = filas if filas is not None else range(self.matriz_distancias.shape[0])
        columnas = columnas if columnas is not None else range(self.matriz_distancias.shape[1])

        # Extraer y mostrar la submatriz
        submatriz = self.matriz_distancias[np.ix_(filas, columnas)]
        print(submatriz)
