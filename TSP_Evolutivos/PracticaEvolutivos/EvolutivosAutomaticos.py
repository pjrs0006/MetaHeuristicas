import os
import importlib
import time
from Ciudad import Ciudad
from Mapa import Mapa
import logging

class evolutivos_automaticos:

    # Definimos el construcrtor de la clase
    def __init__(self):
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
        ruta_config = os.path.join('recursos', 'archivosConf', 'ficheroConfiguracion.txt')
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



        # Seleccionar archivo TSP
        print("Mostrando los archivos TSP disponibles en el directorio:")
        selIndice=0
        for archivo in self.archivos:
            print("\t",selIndice," ",chr(10147),"...............",archivo)
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



        # Ejecutamos iterativamente los 2 algoritmos sobre el tsp seleccionado, en cada vuelta del bucle interno
        # se ejecuta el generacional 8 veces y el estacionario 2 veces, con sus diferentes parametros, y el segundo
        # bucle hara que se ejecute el bucle interno 5 veces, cada vez con una de las semillas.

        #Bucle para cada semilla:
        for semilla in range (5):
        #Primero Seleccionamo el algoritmo evolutivo generacional:
            indice_algoritmo = 3
            nombre_algoritmo = self.algoritmos[indice_algoritmo]


        # Algoritmo Evolutivo Generacional_Version_1:
            print(f"Algoritmo Evolutivo Generacional:")
            print(f"--------------------------------")
            logging.info(f"Algoritmo Evolutivo Generacional:")
            logging.info(f"---------------------------------")
            k = int(5)
            logging.info(f"\t\tK:\t{k}")

            poblacionmax = int(100)
            logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")

            porcentajealeatorio = int(80)
            logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")

            kbest = int(2)
            logging.info(f"\t\tKbest:\t{kbest}")

            kworst = int(3)
            logging.info(f"\t\tkworst:\t{kworst}")

            procruce = int(70)
            logging.info(f"\t\tProcruce:\t{procruce}")

            promut = int(10)
            logging.info(f"\t\tPromut:\t{promut}")

            Evmax = int(50000)
            logging.info(f"\t\tEvmax:\t{Evmax}")

            Tmax = int(60)
            logging.info(f"\t\tTmax:\t{Tmax}")

            tipocruce = int(0)
            if tipocruce == 0:
                logging.info(f"\t\tTipocruce:\tOX2")
            else:
                logging.info(f"\t\tTipocruce:\tMOC")


            elite = int(1)
            logging.info(f"\t\tElite:\t{elite}")

            seed = self.semillas[semilla]
            logging.info(f"\t\tSeed:\t{seed}")

            start_time = time.perf_counter()
            algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                            tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                            porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                            kworst=kworst, procruce=procruce, promut=promut, Evmax=Evmax, Tmax=Tmax,
                                            tipocruce=tipocruce, elite=elite)  # ,num_elites=num_elites)

            end_time = time.perf_counter()
            tiempo = (end_time - start_time)
            mGlobal = algoritmo['ruta']
            mDisGlobal = algoritmo['fitness']

            print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
            logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
            print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
            logging.info(f"\t\tMejor camino: {mGlobal}")
            print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")
            logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        # Algoritmo Evolutivo Generacional_Version_2:
        print(f"Algoritmo Evolutivo Generacional:")
        print(f"--------------------------------")
        logging.info(f"Algoritmo Evolutivo Generacional:")
        logging.info(f"---------------------------------")
        k = int(5)
        logging.info(f"\t\tK:\t{k}")

        poblacionmax = int(100)
        logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")

        porcentajealeatorio = int(80)
        logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")

        kbest = int(3)
        logging.info(f"\t\tKbest:\t{kbest}")

        kworst = int(3)
        logging.info(f"\t\tkworst:\t{kworst}")

        procruce = int(70)
        logging.info(f"\t\tProcruce:\t{procruce}")

        promut = int(10)
        logging.info(f"\t\tPromut:\t{promut}")

        Evmax = int(50000)
        logging.info(f"\t\tEvmax:\t{Evmax}")

        Tmax = int(60)
        logging.info(f"\t\tTmax:\t{Tmax}")

        tipocruce = int(0)
        if tipocruce == 0:
            logging.info(f"\t\tTipocruce:\tOX2")
        else:
            logging.info(f"\t\tTipocruce:\tMOC")

        elite = int(1)
        logging.info(f"\t\tElite:\t{elite}")

        seed = self.semillas[semilla]
        logging.info(f"\t\tSeed:\t{seed}")

        start_time = time.perf_counter()
        algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                            tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                            porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                            kworst=kworst, procruce=procruce, promut=promut, Evmax=Evmax, Tmax=Tmax,
                                            tipocruce=tipocruce, elite=elite)  # ,num_elites=num_elites)

        end_time = time.perf_counter()
        tiempo = (end_time - start_time)
        mGlobal = algoritmo['ruta']
        mDisGlobal = algoritmo['fitness']

        print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
        logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
        print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
        logging.info(f"\t\tMejor camino: {mGlobal}")
        print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")
        logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        # Algoritmo Evolutivo Generacional_Version_3:
        print(f"Algoritmo Evolutivo Generacional:")
        print(f"--------------------------------")
        logging.info(f"Algoritmo Evolutivo Generacional:")
        logging.info(f"---------------------------------")
        k = int(5)
        logging.info(f"\t\tK:\t{k}")

        poblacionmax = int(100)
        logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")

        porcentajealeatorio = int(80)
        logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")

        kbest = int(2)
        logging.info(f"\t\tKbest:\t{kbest}")

        kworst = int(3)
        logging.info(f"\t\tkworst:\t{kworst}")

        procruce = int(70)
        logging.info(f"\t\tProcruce:\t{procruce}")

        promut = int(10)
        logging.info(f"\t\tPromut:\t{promut}")

        Evmax = int(50000)
        logging.info(f"\t\tEvmax:\t{Evmax}")

        Tmax = int(60)
        logging.info(f"\t\tTmax:\t{Tmax}")

        tipocruce = int(0)
        if tipocruce == 0:
            logging.info(f"\t\tTipocruce:\tOX2")
        else:
            logging.info(f"\t\tTipocruce:\tMOC")

        elite = int(2)
        logging.info(f"\t\tElite:\t{elite}")

        seed = self.semillas[semilla]
        logging.info(f"\t\tSeed:\t{seed}")

        start_time = time.perf_counter()
        algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                            tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                            porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                            kworst=kworst, procruce=procruce, promut=promut, Evmax=Evmax, Tmax=Tmax,
                                            tipocruce=tipocruce, elite=elite)  # ,num_elites=num_elites)

        end_time = time.perf_counter()
        tiempo = (end_time - start_time)
        mGlobal = algoritmo['ruta']
        mDisGlobal = algoritmo['fitness']

        print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
        logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
        print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
        logging.info(f"\t\tMejor camino: {mGlobal}")
        print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")
        logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        # Algoritmo Evolutivo Generacional_Version_4:
        print(f"Algoritmo Evolutivo Generacional:")
        print(f"--------------------------------")
        logging.info(f"Algoritmo Evolutivo Generacional:")
        logging.info(f"---------------------------------")
        k = int(5)
        logging.info(f"\t\tK:\t{k}")

        poblacionmax = int(100)
        logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")

        porcentajealeatorio = int(80)
        logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")

        kbest = int(3)
        logging.info(f"\t\tKbest:\t{kbest}")

        kworst = int(3)
        logging.info(f"\t\tkworst:\t{kworst}")

        procruce = int(70)
        logging.info(f"\t\tProcruce:\t{procruce}")

        promut = int(10)
        logging.info(f"\t\tPromut:\t{promut}")

        Evmax = int(50000)
        logging.info(f"\t\tEvmax:\t{Evmax}")

        Tmax = int(60)
        logging.info(f"\t\tTmax:\t{Tmax}")

        tipocruce = int(0)
        if tipocruce == 0:
            logging.info(f"\t\tTipocruce:\tOX2")
        else:
            logging.info(f"\t\tTipocruce:\tMOC")

        elite = int(2)
        logging.info(f"\t\tElite:\t{elite}")

        seed = self.semillas[semilla]
        logging.info(f"\t\tSeed:\t{seed}")

        start_time = time.perf_counter()
        algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                            tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                            porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                            kworst=kworst, procruce=procruce, promut=promut, Evmax=Evmax, Tmax=Tmax,
                                            tipocruce=tipocruce, elite=elite)  # ,num_elites=num_elites)

        end_time = time.perf_counter()
        tiempo = (end_time - start_time)
        mGlobal = algoritmo['ruta']
        mDisGlobal = algoritmo['fitness']

        print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
        logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
        print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
        logging.info(f"\t\tMejor camino: {mGlobal}")
        print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")
        logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        # Algoritmo Evolutivo Generacional_Version_5:
        print(f"Algoritmo Evolutivo Generacional:")
        print(f"--------------------------------")
        logging.info(f"Algoritmo Evolutivo Generacional:")
        logging.info(f"---------------------------------")
        k = int(5)
        logging.info(f"\t\tK:\t{k}")

        poblacionmax = int(100)
        logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")

        porcentajealeatorio = int(80)
        logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")

        kbest = int(2)
        logging.info(f"\t\tKbest:\t{kbest}")

        kworst = int(3)
        logging.info(f"\t\tkworst:\t{kworst}")

        procruce = int(70)
        logging.info(f"\t\tProcruce:\t{procruce}")

        promut = int(10)
        logging.info(f"\t\tPromut:\t{promut}")

        Evmax = int(50000)
        logging.info(f"\t\tEvmax:\t{Evmax}")

        Tmax = int(60)
        logging.info(f"\t\tTmax:\t{Tmax}")

        tipocruce = int(1)
        if tipocruce == 0:
            logging.info(f"\t\tTipocruce:\tOX2")
        else:
            logging.info(f"\t\tTipocruce:\tMOC")

        elite = int(1)
        logging.info(f"\t\tElite:\t{elite}")

        seed = self.semillas[semilla]
        logging.info(f"\t\tSeed:\t{seed}")

        start_time = time.perf_counter()
        algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                            tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                            porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                            kworst=kworst, procruce=procruce, promut=promut, Evmax=Evmax, Tmax=Tmax,
                                            tipocruce=tipocruce, elite=elite)  # ,num_elites=num_elites)

        end_time = time.perf_counter()
        tiempo = (end_time - start_time)
        mGlobal = algoritmo['ruta']
        mDisGlobal = algoritmo['fitness']

        print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
        logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
        print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
        logging.info(f"\t\tMejor camino: {mGlobal}")
        print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")
        logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        # Algoritmo Evolutivo Generacional_Version_6:
        print(f"Algoritmo Evolutivo Generacional:")
        print(f"--------------------------------")
        logging.info(f"Algoritmo Evolutivo Generacional:")
        logging.info(f"---------------------------------")
        k = int(5)
        logging.info(f"\t\tK:\t{k}")

        poblacionmax = int(100)
        logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")

        porcentajealeatorio = int(80)
        logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")

        kbest = int(3)
        logging.info(f"\t\tKbest:\t{kbest}")

        kworst = int(3)
        logging.info(f"\t\tkworst:\t{kworst}")

        procruce = int(70)
        logging.info(f"\t\tProcruce:\t{procruce}")

        promut = int(10)
        logging.info(f"\t\tPromut:\t{promut}")

        Evmax = int(50000)
        logging.info(f"\t\tEvmax:\t{Evmax}")

        Tmax = int(60)
        logging.info(f"\t\tTmax:\t{Tmax}")

        tipocruce = int(1)
        if tipocruce == 0:
            logging.info(f"\t\tTipocruce:\tOX2")
        else:
            logging.info(f"\t\tTipocruce:\tMOC")

        elite = int(1)
        logging.info(f"\t\tElite:\t{elite}")

        seed = self.semillas[semilla]
        logging.info(f"\t\tSeed:\t{seed}")

        start_time = time.perf_counter()
        algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                            tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                            porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                            kworst=kworst, procruce=procruce, promut=promut, Evmax=Evmax, Tmax=Tmax,
                                            tipocruce=tipocruce, elite=elite)  # ,num_elites=num_elites)

        end_time = time.perf_counter()
        tiempo = (end_time - start_time)
        mGlobal = algoritmo['ruta']
        mDisGlobal = algoritmo['fitness']

        print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
        logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
        print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
        logging.info(f"\t\tMejor camino: {mGlobal}")
        print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")
        logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        # Algoritmo Evolutivo Generacional_Version_7:
        print(f"Algoritmo Evolutivo Generacional:")
        print(f"--------------------------------")
        logging.info(f"Algoritmo Evolutivo Generacional:")
        logging.info(f"---------------------------------")
        k = int(5)
        logging.info(f"\t\tK:\t{k}")

        poblacionmax = int(100)
        logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")

        porcentajealeatorio = int(80)
        logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")

        kbest = int(3)
        logging.info(f"\t\tKbest:\t{kbest}")

        kworst = int(3)
        logging.info(f"\t\tkworst:\t{kworst}")

        procruce = int(70)
        logging.info(f"\t\tProcruce:\t{procruce}")

        promut = int(10)
        logging.info(f"\t\tPromut:\t{promut}")

        Evmax = int(50000)
        logging.info(f"\t\tEvmax:\t{Evmax}")

        Tmax = int(60)
        logging.info(f"\t\tTmax:\t{Tmax}")

        tipocruce = int(1)
        if tipocruce == 0:
            logging.info(f"\t\tTipocruce:\tOX2")
        else:
            logging.info(f"\t\tTipocruce:\tMOC")

        elite = int(2)
        logging.info(f"\t\tElite:\t{elite}")

        seed = self.semillas[semilla]
        logging.info(f"\t\tSeed:\t{seed}")

        start_time = time.perf_counter()
        algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                            tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                            porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                            kworst=kworst, procruce=procruce, promut=promut, Evmax=Evmax, Tmax=Tmax,
                                            tipocruce=tipocruce, elite=elite)  # ,num_elites=num_elites)

        end_time = time.perf_counter()
        tiempo = (end_time - start_time)
        mGlobal = algoritmo['ruta']
        mDisGlobal = algoritmo['fitness']

        print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
        logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
        print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
        logging.info(f"\t\tMejor camino: {mGlobal}")
        print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")
        logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        # Algoritmo Evolutivo Generacional_Version_8:
        print(f"Algoritmo Evolutivo Generacional:")
        print(f"--------------------------------")
        logging.info(f"Algoritmo Evolutivo Generacional:")
        logging.info(f"---------------------------------")
        k = int(5)
        logging.info(f"\t\tK:\t{k}")

        poblacionmax = int(100)
        logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")

        porcentajealeatorio = int(80)
        logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")

        kbest = int(3)
        logging.info(f"\t\tKbest:\t{kbest}")

        kworst = int(3)
        logging.info(f"\t\tkworst:\t{kworst}")

        procruce = int(70)
        logging.info(f"\t\tProcruce:\t{procruce}")

        promut = int(10)
        logging.info(f"\t\tPromut:\t{promut}")

        Evmax = int(50000)
        logging.info(f"\t\tEvmax:\t{Evmax}")

        Tmax = int(60)
        logging.info(f"\t\tTmax:\t{Tmax}")

        tipocruce = int(1)
        if tipocruce == 0:
            logging.info(f"\t\tTipocruce:\tOX2")
        else:
            logging.info(f"\t\tTipocruce:\tMOC")

        elite = int(2)
        logging.info(f"\t\tElite:\t{elite}")

        seed = self.semillas[semilla]
        logging.info(f"\t\tSeed:\t{seed}")

        start_time = time.perf_counter()
        algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                            tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                            porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                            kworst=kworst, procruce=procruce, promut=promut, Evmax=Evmax, Tmax=Tmax,
                                            tipocruce=tipocruce, elite=elite)  # ,num_elites=num_elites)

        end_time = time.perf_counter()
        tiempo = (end_time - start_time)
        mGlobal = algoritmo['ruta']
        mDisGlobal = algoritmo['fitness']

        print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
        logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
        print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
        logging.info(f"\t\tMejor camino: {mGlobal}")
        print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")
        logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        indice_algoritmo = 4
        nombre_algoritmo = self.algoritmos[indice_algoritmo]

        #Algoritmo Evolutivo Estacionario_Version_1
        print(f"Algoritmo evolutivoestacionario:")
        print(f"---------------------------")
        logging.info(f"Algoritmo evolutivoestacionario:")
        logging.info(f"-------------------------------")
        k = int(5)
        logging.info(f"\t\tK:\t{k}")

        poblacionmax = int(100)
        logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")

        porcentajealeatorio = int(80)
        logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")

        kbest = int(2)
        logging.info(f"\t\tKbest:\t{kbest}")

        kworst = int(2)
        logging.info(f"\t\tkworst:\t{kworst}")

        procruce = int(70)
        logging.info(f"\t\tProcruce:\t{procruce}")

        promut = int(10)
        logging.info(f"\t\tPromut:\t{promut}")

        Evmax = int(50000)
        logging.info(f"\t\tEvmax:\t{Evmax}")

        Tmax = int(60)
        logging.info(f"\t\tTmax:\t{Tmax}")

        tipocruce = int(0)
        if tipocruce == 0:
            logging.info(f"\t\tTipocruce:\tOX2")
        else:
            logging.info(f"\t\tTipocruce:\tMOC")

        seed = self.semillas[semilla]
        logging.info(f"\t\tSeed:\t{seed}")

        start_time = time.perf_counter()
        algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                            tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                            porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                            kworst=kworst, promut=promut, Evmax=Evmax,
                                            Tmax=Tmax, tipocruce=tipocruce)

        end_time = time.perf_counter()
        tiempo = (end_time - start_time)
        mGlobal = algoritmo['ruta']
        mDisGlobal = algoritmo['fitness']

        print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
        logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
        print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
        logging.info(f"\t\tMejor camino: {mGlobal}")
        print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")
        logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        # Algoritmo Evolutivo Estacionario_Version_2
        print(f"Algoritmo evolutivoestacionario:")
        print(f"---------------------------")
        logging.info(f"Algoritmo evolutivoestacionario:")
        logging.info(f"-------------------------------")
        k = int(5)
        logging.info(f"\t\tK:\t{k}")

        poblacionmax = int(100)
        logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")

        porcentajealeatorio = int(80)
        logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")

        kbest = int(2)
        logging.info(f"\t\tKbest:\t{kbest}")

        kworst = int(2)
        logging.info(f"\t\tkworst:\t{kworst}")

        procruce = int(70)
        logging.info(f"\t\tProcruce:\t{procruce}")

        promut = int(10)
        logging.info(f"\t\tPromut:\t{promut}")

        Evmax = int(50000)
        logging.info(f"\t\tEvmax:\t{Evmax}")

        Tmax = int(60)
        logging.info(f"\t\tTmax:\t{Tmax}")

        tipocruce = int(1)
        if tipocruce == 0:
            logging.info(f"\t\tTipocruce:\tOX2")
        else:
            logging.info(f"\t\tTipocruce:\tMOC")

        seed = self.semillas[semilla]
        logging.info(f"\t\tSeed:\t{seed}")

        start_time = time.perf_counter()
        algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                            tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                            porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                            kworst=kworst, promut=promut, Evmax=Evmax,
                                            Tmax=Tmax, tipocruce=tipocruce)

        end_time = time.perf_counter()
        tiempo = (end_time - start_time)
        mGlobal = algoritmo['ruta']
        mDisGlobal = algoritmo['fitness']

        print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
        logging.info(f"\t\tTiempo de ejecucion: {tiempo:.4f} segundos")
        print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
        logging.info(f"\t\tMejor camino: {mGlobal}")
        print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")
        logging.info(f"\t\tDistancia del mejor camino: {mDisGlobal:.2f}")

        #Ejecuciones concluidas:
        print(f"Se han concluido todas las ejecuciones sobre el fichero {mapautilizado.nombre}")
