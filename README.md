Representacion de la solucion: mapa de ciudades
							   matriz de distancias

objetivo: minimizar la distancia del recorrido, pasando por todas las ciudades sin 
repetirlas y volver al origen 


¿Que hay que hacer?

1. Crear la clase ciudad atr(numero, x,y )
   metodos: 
		Constructores destructores
		getter setter 
		
2. crear la clase Mapa atr(list<ciudad>)
   metodos: 
		constructor(list<ficheros>) : Debe cargar las ciudades que hay en los ficheros 
        float conseguirdistancia() -> devuelve la distancia entre dos ciudades dadas

Ayudas: 
 Lista para almacenar múltiples valores
        self.lista_datos = []

         Diccionario para asociar claves con valores
        self.diccionario_datos = {}
		
		Conjunto para almacenar valores únicos
        self.conjunto_datos = set()