from Ciudad import Ciudad
import numpy as np
import math
##
#  \class Mapa
#  \brief Clase que representa un mapa con ciudades y una matriz de distancias entre ellas.
#
#  La clase Mapa gestiona una colección de ciudades y calcula las distancias entre ellas.
#  También permite mostrar una submatriz de distancias.
#
class Mapa:

    ##
    #  \brief Constructor de la clase.
    #
    #  Inicializa un nuevo mapa con un diccionario vacío para almacenar las ciudades y
    #  una matriz de distancias inicializada con infinito.
    #
    def __init__(self):
        self.ciudades = {}
        self.matriz_distancias = np.inf
        # Ahora añadimos los atributos correspondientes a la cabezera del archivo .tsp
        self.nombre = None
        self.comentario = None
        self.tipo = None
        self.tam = None
        self.edge_type = None
    ##
    #  \brief Añade una nueva ciudad al mapa.
    #
    #  \param nuevaciudad Objeto de la clase Ciudad que se va a añadir al mapa.
    #         La ciudad se identifica por su ID.
    #
    def nueva_ciudad(self, nuevaciudad):
        self.ciudades[nuevaciudad.id] = nuevaciudad

    ##
    #  \brief Calcula la distancia euclidiana entre dos ciudades.
    #
    #  \param C1 Objeto de la clase Ciudad que representa la primera ciudad.
    #  \param C2 Objeto de la clase Ciudad que representa la segunda ciudad.
    #
    #  \return La distancia euclidiana entre las dos ciudades.
    #
    def calculadistancia(self, C1, C2):
        x1, y1 = C1.x, C1.y
        x2, y2 = C2.x, C2.y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    ##
    #  \brief Muestra una submatriz de distancias entre las ciudades.
    #
    #  \param filas Lista de índices de filas a mostrar. Si es None, se muestran todas las filas.
    #  \param columnas Lista de índices de columnas a mostrar. Si es None, se muestran todas las columnas.
    #
    #  Si no se especifican filas o columnas, se muestra la matriz completa de distancias.
    #
    def mostrar_matriz(self, filas=None, columnas=None):
        # Usar la lista completa si `filas` o `columnas` no se especifican
        # shape es un atributo del array que devuelve el tamaño del mismo
        filas = filas if filas is not None else range(self.matriz_distancias.shape[0])
        columnas = columnas if columnas is not None else range(self.matriz_distancias.shape[1])

        # Extraer y mostrar la submatriz
        submatriz = self.matriz_distancias[np.ix_(filas, columnas)]
        print(submatriz)

