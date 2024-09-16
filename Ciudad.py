## \file Ciudad.py
#  \brief Este archivo contiene la definición de la clase Ciudad.
#
#  La clase Ciudad representa una ubicación en un plano con coordenadas (x, y)
#  y un identificador único. La clase incluye métodos para obtener y modificar
#  estos atributos.
#

## \class Ciudad
#  \brief Clase que representa una ciudad con un identificador y coordenadas en un plano.
#
#  La clase Ciudad tiene tres atributos principales: un identificador único (\a id),
#  y las coordenadas \a x e \a y en un plano. También proporciona métodos
#  para obtener y establecer estos valores.
#
class Ciudad:

    ## \brief Constructor de la clase.
    #
    #  Inicializa una ciudad con un \a id, y las coordenadas \a x e \a y.
    #  \param id El identificador único de la ciudad (debe ser positivo).
    #  \param x La coordenada x de la ciudad.
    #  \param y La coordenada y de la ciudad.
    #
    def __init__(self, id, x, y):
        self.id = int(id)
        self.x = int(x)
        self.y = int(y)

    ## \brief Obtiene el identificador de la ciudad.
    #  \return El \a id de la ciudad.
    #
    def getid(self):
        return self.id

    ## \brief Obtiene la coordenada x de la ciudad.
    #  \return La coordenada \a x de la ciudad.
    #
    def getx(self):
        return self.x

    ## \brief Obtiene la coordenada y de la ciudad.
    #  \return La coordenada \a y de la ciudad.
    #
    def gety(self):
        return self.y

    ## \brief Establece el identificador de la ciudad.
    #
    #  El identificador debe ser un valor positivo.
    #  \param id El nuevo identificador de la ciudad.
    #
    def setid(self, id):
        if id > 0:
            self.id = id
        else:
            print("El id no puede ser negativo")

    ## \brief Establece la coordenada x de la ciudad.
    #  \param x La nueva coordenada \a x de la ciudad.
    #
    def setx(self, x):
        self.x = x

    ## \brief Establece la coordenada y de la ciudad.
    #  \param y La nueva coordenada \a y de la ciudad.
    #
    def sety(self, y):
        self.y = y
