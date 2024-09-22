Práctica 1

La práctica se trabajará con el problema del viajante de comercio (TSP) donde la pareja de alumnos deberá desarrollar los algoritmos de la práctica siguiendo la modalidad que desee: trabajando con cualquiera de los frameworks de metaheurísticas estudiados en el Seminario 1, implementándolos a partir de código propio o considerando cualquier código disponible en Internet .

Los algoritmos desarrollados serán probados sobre una serie de instancias del problema. Se realizará un estudio comparativo de los resultados obtenidos y se analizará el comportamiento de cada algoritmo en base a dichos resultados. Este análisis influirá decisivamente en la calificación final de la práctica. 

En las secciones siguientes se describen el problema y los casos considerados, los aspectos relacionados con cada algoritmo a desarrollar y las tablas de resultados a obtener.

OBJETIVOS
El objetivo de esta práctica es estudiar el funcionamiento de un algoritmo greedy aleatorio, técnicas de búsqueda local y metaheurísticas basadas en trayectorias en la resolución del problema descrito en las transparencias del Seminario 2. Para ello, se requerirá que el estudiante implemente los algoritmos a dicho problema:

●    Algoritmo greedy aleatorio
●    Algoritmo de búsqueda local del mejor
●    Algoritmo de búsqueda tabú
●    Algoritmo de trayectorias múltiples

La fecha límite de entrega será el viernes 18 de octubre de 2024 antes de las 23:00 horas. La entrega se realizará a través de la plataforma virtual.


CASOS DE ESTUDIO
Dentro del material de las prácticas se encuentran disponibles distintos problemas con distinto tamaño.

El formato de los ficheros puede ser analizado en el documento del Seminario 2. Para cada problema se cuenta con el fichero de datos de distancias euclídeas entre las distancias y un fichero con la mejor solución encontrada para cada problema.

La forma en que habitualmente se estima la calidad de un algoritmo es la siguiente: se ejecuta sobre un conjunto de ejemplos y se comparan los resultados obtenidos con las mejores soluciones conocidas para dichos problemas.

Además, los algoritmos pueden tener diversos parámetros o pueden emplear diversas estrategias. Para determinar qué valor es el más adecuado para un parámetro o saber la estrategia más efectiva los algoritmos también se comparan entre sí.

La comparación de los algoritmos se lleva a cabo fundamentalmente usando dos criterios, la calidad de las soluciones obtenidas y el tiempo de ejecución empleado para conseguirlas. Además, es posible que los algoritmos no se comporten de la misma forma si se ejecutan sobre un conjunto de instancias u otro.

Por otro lado, a diferencia de los algoritmos determinísticos, los algoritmos probabilísticos se caracterizan por la toma de decisiones aleatorias a lo largo de su ejecución. Este hecho implica que un mismo algoritmo probabilístico aplicado al mismo caso de un problema pueda comportarse de forma diferente y por tanto proporcionar resultados distintos en cada ejecución. Cuando se analiza el comportamiento de una metaheurística probabilística en un caso de un problema, se desearía que el resultado obtenido no estuviera sesgado por una secuencia aleatoria concreta que pueda influir positiva o negativamente en las decisiones tomadas durante su ejecución. 

Dada la influencia de la aleatoriedad en el proceso, es recomendable disponer de un generador de secuencia pseudoaleatoria de buena calidad con el que, dado un valor semilla de inicialización, se obtengan números en una secuencia lo suficientemente grande (es decir, que no se repitan los números en un margen razonable) como para considerarse aleatoria. 

Como norma general, el proceso a seguir consiste en realizar un número de ejecuciones diferentes de cada algoritmo probabilístico considerado para cada caso del problema. Es necesario asegurarse de que se realizan diferentes secuencias aleatorias en dichas ejecuciones. Así, el valor de la semilla que determina la inicialización de cada secuencia deberá ser distinto en cada ejecución y estas semillas deben mantenerse en los distintos algoritmos (es decir, la semilla para la primera ejecución de todos los algoritmos debe ser la misma, la de la segunda también debe ser la misma y distinta de la anterior, etc.). Para mostrar los resultados obtenidos con cada algoritmo en el que se hayan realizado varias ejecuciones, se deben construir tablas que recojan los valores correspondientes a estadísticos como el mejor y peor resultado para cada caso del problema, así como la media y la desviación típica de todas las ejecuciones. Alternativamente, se pueden emplear descripciones más representativas como los boxplots, que proporcionan información de todas las ejecuciones realizadas mostrando mínimo, máximo, mediana y primer y tercer cuartil de forma gráfica, Finalmente, se construirán unas tablas globales con los resultados agregados que mostrarán la calidad del algoritmo en la resolución del problema desde un punto de vista general.

Este será el procedimiento que aplicaremos en las prácticas. Como norma general, el alumno realizará 5 ejecuciones diferentes de cada algoritmo probabilístico considerado para cada caso del problema. Se considerará como semilla inicial el número del DNI del alumno. En la tabla 2 se incluye un ejemplo sobre los posibles valores de la semilla para el generador aleatorio.

Tabla 2: Ejemplo de posibles semillas a utilizar en el generador aleatorio

Ejecución	Semilla
1	12345678
2	23456781
3	34567812
4	45678123
5	56781234
ALGORITMOS
1. ALGORITMO GREEDY ALEATORIO
Se debe resolver el problema planteado mediante una solución Greedy ALEATORIA. En concreto, vamos a utilizar la idea de crear las soluciones a partir de una aleatoria seleccionada de entre las más prometedoras.

En primer lugar, se calcula un vector ordenado formado por un par: <ciudad, distancia_al_resto_de_ciudades>, es decir, un vector ordenado donde tenemos la ciudad y la sumatoria de la distancia al resto de ciudades.

Posteriormente, vamos construyendo la ciudad a partir de elegir de forma aleatoria una de entre las K con la distancia más corta. La K tendrá un valor de 5.

Ejemplo

Creamos el vector ordenador y tenemos un vector con un problema de 100 ciudades a visitar (por ejemplo: 3 98 7 19 100 54 34 ... 25), y para elegir la primera ciudad de la solución generamos un aleatorio entre 1 y K, y el valor que nos de la operación actual (por ejemplo 3) nos indica la primera ciudad a visitar, es decir, ciudad 7. Este proceso lo repetimos hasta completar la solución completa.

NOTA: En la segunda iteración el vector elimina del mismo la ciudad 7 para no volver a ser elegida.
