import os
import importlib
import time
from Ciudad import Ciudad
from Mapa import Mapa
import logging

class EjecucionesAutomaticas:


    def __init__(self):
        # Definimos el nivel y formato de los loggins
        logging.basicConfig(
            filename='EjecucionesAutomaticas.log',
            level=logging.DEBUG,
            format='%(message)s'
        )

        self.archivos = []
        self.semillas = []
        self.algoritmos = []
        self.parametros = []
    # La siguiente función lee el archivo de configuración
    def leer_archivo_config(self, ruta_config):
        if os.path.isfile(ruta_config):
            with open(ruta_config, "r") as archivo_config:
                for linea in archivo_config:
                    linea = linea.strip()
                    if "Archivos=" in linea:
                        self.archivos = linea.split("=")[1].strip().split()
                    elif "Semillas=" in linea:
                        self.semillas = list(map(int, linea.split("=")[1].strip().split()))
                    elif "Algoritmos=" in linea:
                        self.algoritmos = linea.split("=")[1].strip().split()
                    elif "otroparametros=" in linea:
                        self.parametros = linea.split("=")[1].strip().split()
        else:
            logging.critical(f"El archivo de configuración {ruta_config} no existe.")
            raise FileNotFoundError(f"El archivo de configuración {ruta_config} no existe.")

    # El siguiente metodo lee y procesa los .tsp
    def leer_archivo(self, archivo):
        miMapa = Mapa()
        seccionCoordenadas = False

        with open(archivo, "r") as archivo_tsp:
            for linea in archivo_tsp:
                linea = linea.strip()

                if linea == "NODE_COORD_SECTION":
                    seccionCoordenadas = True
                    continue

                if linea == "EOF":
                    break

                if not seccionCoordenadas:
                    if ":" in linea:
                        clave, valor = linea.split(":", 1)
                        clave = clave.strip().upper()
                        valor = valor.strip()

                        if clave == "NAME":
                            miMapa.nombre = valor
                        elif clave == "COMMENT":
                            miMapa.comentario = valor
                        elif clave == "TYPE":
                            miMapa.tipo = valor
                        elif clave == "DIMENSION":
                            miMapa.tam = int(valor)
                        elif clave == "EDGE_WEIGHT_TYPE":
                            miMapa.edge_type = valor
                else:
                    partes = linea.split()
                    if len(partes) == 3:
                        id_nodo = int(partes[0])
                        x = float(partes[1])
                        y = float(partes[2])
                        ciudad = Ciudad(id_nodo, x, y)
                        miMapa.ciudades[id_nodo] = ciudad
        print("Archivo procesado con éxito.")
        return miMapa

    # Metodo que imprime el mapa
    def imprimirMapa(self, miMapa):
        print(f"\tNombre: {miMapa.nombre}")
        logging.info(f"\tNombre: {miMapa.nombre}")
        print(f"\tComentario: {miMapa.comentario}")
        logging.info(f"\tComentario: {miMapa.comentario}")
        print(f"\tTipo: {miMapa.tipo}")
        logging.info(f"\tTipo: {miMapa.tipo}")
        print(f"\tDimensión: {miMapa.tam}")
        logging.info(f"\tDimension: {miMapa.tam}")
        print(f"\tTipo de peso de arista: {miMapa.edge_type}")
        logging.info(f"\tTipo de peso de arista: {miMapa.edge_type}")
        print("\tCoordenadas de las ciudades:")
        logging.info(f"\tCoordenadas de las ciudades:")
        for ciudad in miMapa.ciudades.values():
            print(f"\t\tID: {ciudad.id}, X: {ciudad.x}, Y: {ciudad.y}")
            logging.info(f"\t\tID: {ciudad.id}, X: {ciudad.x}, Y: {ciudad.y}")

    # Metodo para ejecutar dinamicamente un algoritmo
    def ejecutar_algoritmo(self, nombre_algoritmo, *args, **kwargs):
        modulo = importlib.import_module(f"algoritmos.{nombre_algoritmo.lower()}")
        clase_algoritmo = getattr(modulo, nombre_algoritmo)
        instancia = clase_algoritmo(*args, **kwargs)
        return instancia.ejecutar()

    # Metodo principal que ejecuta la logica completa
    def ejecutar(self):
        # Rutas de configuración y TSP
        ruta_config = os.path.join('recursos', 'archivosConf', 'Config_1.txt')
        ruta_tsp = os.path.join('recursos', 'archivosTSP')
        logging.warning(f"Comenzando ejecuciones")
        # Leer archivo de configuración
        self.leer_archivo_config(ruta_config)
        logging.info(f"Fichero de configuracion procesado con exito")

        # Validaciones
        if not self.archivos:
            logging.critical("No se han especificado archivos en la configuración.")
            raise ValueError("No se han especificado archivos en la configuración.")
        if not self.algoritmos:
            logging.critical("No se han especificado algoritmos en la configuración.")
            raise ValueError("No se han especificado algoritmos en la configuración.")

        if not self.parametros or len(self.parametros) < 11:
            logging.critical("Los parámetros de configuración son insuficientes.")
            raise ValueError("Los parámetros de configuración son insuficientes.")

        # Seleccionar archivo TSP
        print("Mostrando los archivos TSP disponibles en el directorio:")
        selIndice=0
        for archivo in self.archivos:
            print("\t",selIndice,chr(10147),"...............",archivo)
            selIndice+=1
        indice_archivo=int(input("Seleccione el archivo sobre el que desea realizar las ejecuciones de los distintos algoritmos:\t"))
        #Cargamos el archivo seleccionado por el usuario:
        archivo_seleccionado = self.archivos[indice_archivo]
        ruta_archivo_tsp = os.path.join(ruta_tsp, archivo_seleccionado)

        if not os.path.isfile(ruta_archivo_tsp):
            raise FileNotFoundError(f"El archivo TSP {ruta_archivo_tsp} no existe.")

        # Leer y procesar el archivo TSP
        mapautilizado = self.leer_archivo(ruta_archivo_tsp)

        # Mostrar los datos del mapa
        print("El mapa sobre el que trabajaremos sera:")
        self.imprimirMapa(mapautilizado)

        # Generar la matriz de distancias
        matriz_d = mapautilizado.generar_matriz_distancias()
        print(f"Matriz de Distancias correspondiente al Mapa {mapautilizado.nombre}")
        logging.info("Matriz de distancias generada con exito")
        # Imprimimos la matriz de distancias
        #for fila in matriz_d:
            #print('\t'.join(map(str, fila)))
            #logging.info('\t'.join(map(str, fila)))

        # Comenzamos la ejecucion con el primer algoritmo
        indice_algoritmo = 0
        nombre_algoritmo = self.algoritmos[indice_algoritmo]


        # Ejecutamos iterativamente los 3 algoritmos sobre el tsp seleccionado, cada uno lo ejecutamos 5 veces con 5 semillas distintas

        #Algoritmo Greedy Aleatorio
        print(f"Algoritmo Greedy Aleatorio:")
        print(f"---------------------------")
        logging.info(f"Algoritmo Greedy Aleatorio:")
        logging.info(f"---------------------------")
        k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
        logging.info(f"\tParametros del Algoritmo:")
        logging.info(f"\t\tK:\t{k}")
        for i in range(5):
            seed = self.semillas[i]
            print(f"{chr(9635)} Ejecucion numero {i+1} del algoritmo Greedy Aleatorio sobre el fichero {mapautilizado.nombre}, con la semilla {seed}:")
            logging.info(f"\tEjecucion numero {i+1} del algoritmo Greedy Aleatorio sobre el fichero {mapautilizado.nombre}, con la semilla {seed}:")
            start_time = time.perf_counter()
            algoritmo = self.ejecutar_algoritmo(nombre_algoritmo,
                                                matriz_distancias=matriz_d,
                                                k=k,
                                                seed=seed,
                                                tam=mapautilizado.tam)
            end_time = time.perf_counter()
            tiempo = end_time - start_time
            print(f"\t{chr(223)}Tiempo de ejecución: {tiempo:.4f} segundos")
            logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
            print(f"\t{chr(223)}Distancia Total: {algoritmo:.2f}")
            logging.info(f"\t\tDistancia Total: {algoritmo:.2f}")

        #Busqueda Local
        print(f"Algoritmo de Busqueda Local:")
        print(f"----------------------------")
        logging.info(f"Algoritmo de Busqueda Local:")
        logging.info(f"----------------------------")
        #Seleccionamos el algoritmo:
        indice_algoritmo = 1
        nombre_algoritmo = self.algoritmos[indice_algoritmo]
        logging.info(f"\tParametros del Algoritmo:")

        k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
        logging.info(f"\t\tK:\t{k}")
        maxit = int(self.parametros[4])
        logging.info(f"\t\tNumero iteraciones:\t{maxit}")
        tamentorno = int(self.parametros[5])
        logging.info(f"\t\tTam entorno dinamico:\t{tamentorno}")
        dismentorno=self.parametros[6]
        logging.info(f"\t\tDisminucion entorno:\t{dismentorno}")
        itDismin= self.parametros[7]
        logging.info(f"\t\tIndice de disminucion:\t{itDismin}")
        for i in range(5):
            seed = self.semillas[i]
            print(f"{chr(9635)} Ejecucion numero {i+1} del algoritmo de Busqueda Local sobre el fichero {mapautilizado.nombre}, con la semilla {seed}:")
            logging.info(f"\tEjecucion numero {i+1} del algoritmo de Busqueda Local sobre el fichero {mapautilizado.nombre}, con la semilla {seed}:")
            start_time = time.perf_counter()
            algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                                tam=mapautilizado.tam, iteraciones=maxit, tamentorno=tamentorno,
                                                dismentorno=dismentorno, itDismin=itDismin)

            end_time = time.perf_counter()
            tiempo = (end_time - start_time)
            print(f"\t{chr(10147)}Tiempo de ejecución: {tiempo:.4f} segundos")
            logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
            print(f"\t{chr(10147)}Camino optimo: {algoritmo[0]}")
            logging.info(f"\t\tCamino optimo: {algoritmo[0]}")
            print(f"\t{chr(10147)}distancia optima: {algoritmo[1]:.2f}")
            logging.info(f"\t\tdistancia optima: {algoritmo[1]:.2f}")

        # Tabu
        print(f"Algoritmo de Busqueda Tabu:")
        print(f"---------------------------")
        logging.info(f"Algoritmo de Busqueda Tabu:")
        logging.info(f"---------------------------")
        # Seleccionamos el algoritmo:
        indice_algoritmo = 2
        nombre_algoritmo = self.algoritmos[indice_algoritmo]
        logging.info(f"\tParametros del Algoritmo:")
        k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
        logging.info(f"\t\tK:\t{k}")
        tamentorno = int(self.parametros[5])
        logging.info(f"\t\tTam entorno inicial:\t{tamentorno}")
        dismentorno = float(self.parametros[6])
        logging.info(f"\t\tDisminucion del entorno:\t{dismentorno}")
        porcentajel = float(self.parametros[10])
        logging.info(f"\t\tOscilacion Estrategica:\t{porcentajel}")
        iteraciones = int (self.parametros[4])
        logging.info(f"\t\tIteraciones:\t{iteraciones}")
        tendencia=int(self.parametros[9])
        logging.info(f"\t\tTendencia Tabu:\t{tendencia}")
        estanca=int(self.parametros[8])
        logging.info(f"\t\tPorcentaje de estancamiento:\t{estanca}")
        for i in range(5):
            seed = self.semillas[i]
            print(f"{chr(9635)} Ejecucion numero {i + 1} del algoritmo de Busqueda Tabu sobre el fichero {mapautilizado.nombre}, con la semilla {seed}:")
            logging.info(f"\tEjecucion numero {i+1} del algoritmo de Busqueda Tabu sobre el fichero {mapautilizado.nombre}, con la semilla {seed}:")

            start_time = time.perf_counter()
            algoritmo = self.ejecutar_algoritmo(nombre_algoritmo,matriz_distancias=matriz_d,k=k,seed=seed,tam=mapautilizado.tam,iteraciones =iteraciones ,tamentorno=tamentorno,dismentorno=dismentorno,porcentajel=porcentajel,tendencia_tabu=tendencia,estanca=estanca,itDismin=itDismin)
            end_time = time.perf_counter()
            tiempo = (end_time - start_time)
            mGlobal = algoritmo[0]
            mDisGlobal= algoritmo[1]
            print(f"\t{chr(10147)}Tiempo de ejecución: {tiempo:.4f} segundos")
            logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
            print(f"\t{chr(10147)}Mejor camino: {mGlobal}")
            logging.info(f"\t\tMejor camino: {mGlobal}")
            print(f"\t{chr(10147)}Distancia del mejor camino: {mDisGlobal:.2f}")
            logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        #Ejecuciones concluidas:
        print(f"Se han concluido todas las ejecuciones sobre el fichero {mapautilizado.nombre}")
        logging.info(f"Se han concluido todas las ejecuciones sobre el fichero {mapautilizado.nombre}")