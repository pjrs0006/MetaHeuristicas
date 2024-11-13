## Manual 
### Archivo Config_1.txt

En este archivo encontraremos lo siguiente:  
Archivos=a0.tsp a1.tsp a2.tsp ... an-1.tsp  
Semillas=s0 s1 s2 ... sn-1 
Algoritmos=alg0 alg1 alg2 ... algn-1  
otroparametros=p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10

* Archivos contendra el nombre de los archivos que se quieran procesar.  
* Semillas contendra las semillas que se querran usar paras las ejecuciones.  
* Algoritmos los nombres de los algoritmos que se quieran ejecutar. (los nombres de los algoritmos deben estar en minusculas para que funcione todo de forma correcta). 
* Otros parametros contiene los parametros necesarios para que funcione nuestros algoritmos.  

    - p0 es el indice del archivo en el listado anterior (Archivos)
    - p1 es el indice del algoritmo que se quiere ejecutar del listado (Algoritmos).
    - p2 es el indice de la semilla que queramos usar.
    - p3 indica de cuanto sera la ventana de ciudades a considerar en cada paso del algoritmo Greedy aleatorio.
    - p4 indica el numero total de iteraciones permitidas.
    - p5 indica el porcentaje del numero de iteraciones totales que servira como el tamanio del entorno.
    - p6 indica el porcentaje de disminucion del entorno.
    - p7 indica el porcentaje de numero de iteraciones que inidica el inicio de la disminucion.
    - p8 indica el porcentaje de iteraciones sin mejora para considerar estancamiento.
    - p9 indica la tenencia Tabu es decir, el numero de iteraciones que una solucion es tabu.
    - p10 indica el porcentaje para decidir entre diversificacion e intensificacion.

### Modos de uso
Existen 2 modos de uso, el 1 y el 2.  
El modo de uso 1 permite realizar todos los algoritmos automaticamente sobre el mismo fichero, indicando el fichero deseado por la terminal.  
(A tener en cuenta que si se selecciona el archivo D18512 el tiempo de ejecucion se dispara) 

El modo de uso 2 permite realizar la ejecucion sobre el archivo indicado en el configurador con el algoritmo indicado en el configurador  
Este modo permite tambien mostrar los datos de las ciudades e imprimir la matriz de distancias si se desea.  

Para indicar cada modo de uso solo habra que teclear su numero corresponidiente por la terminal o 0 si se quiere cerrar el programa.  

Una vez acabadas las ejecuciones de cualquiera de los dos modos se pulsara la tecla enter para terminar la ejecucion.

## Ejecucion del Ejecutable
Entrar a la carpeta Ejecutable contenida en este proyecto, dentro encontraremos metaTsp.exe que es el archivo ejecutable. Junto a el encontramos dos carpetas una que se llama algoritmos y otra que se llama recursos. Dentro de algoritmos encontraremos los ficheros que contienen el codigo de los algoritmos que se desean ejecutar.
Por otro lado, en la carpeta recursos encontramos otras dos carpetas:
1. archivosConf, que contiene el nuestro archivo de configuracion que utilizaremos para fijar los valores de los parametros.
2. archivosTSP, que contiene los archivos con los datos de ciudades que se desean procesar.

Para ejecutar dar doble click a metaTsp.exe





