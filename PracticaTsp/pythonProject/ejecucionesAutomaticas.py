import os
import importlib
import time
from Ciudad import Ciudad
from Mapa import Mapa

class EjecucionesAutomaticas:
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
        print(f"\tComentario: {miMapa.comentario}")
        print(f"\tTipo: {miMapa.tipo}")
        print(f"\tDimensión: {miMapa.tam}")
        print(f"\tTipo de peso de arista: {miMapa.edge_type}")

        print("\tCoordenadas de las ciudades:")
        for ciudad in miMapa.ciudades.values():
            print(f"\t\tID: {ciudad.id}, X: {ciudad.x}, Y: {ciudad.y}")

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

        # Leer archivo de configuración
        self.leer_archivo_config(ruta_config)

        # Validaciones
        if not self.archivos:
            raise ValueError("No se han especificado archivos en la configuración.")
        if not self.algoritmos:
            raise ValueError("No se han especificado algoritmos en la configuración.")
        if not self.parametros or len(self.parametros) < 3:
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
        # Imprimimos la matriz de distancias
        # for fila in matriz_d:
        #     print('\t'.join(map(str, fila)))

        # Comenzamos la ejecucion con el primer algoritmo
        indice_algoritmo = 0
        nombre_algoritmo = self.algoritmos[indice_algoritmo]


        # Ejecutamos iterativamente los 3 algoritmos sobre el tsp seleccionado, cada uno lo ejecutamos 5 veces con 5 semillas distintas

        #Algoritmo Greedy Aleatorio
        print(f"Algoritmo Greedy Aleatorio:")
        print(f"---------------------------")
        k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
        for i in range(5):
            seed = self.semillas[i]
            print(f"{chr(9635)} Ejecucion numero {i+1} del algoritmo Greedy Aleatorio sobre el fichero {mapautilizado.nombre}, con la semilla {seed}:")
            start_time = time.perf_counter()
            algoritmo = self.ejecutar_algoritmo(nombre_algoritmo,
                                                matriz_distancias=matriz_d,
                                                k=k,
                                                seed=seed,
                                                tam=mapautilizado.tam)
            end_time = time.perf_counter()
            tiempo = end_time - start_time
            print(f"\t{chr(10147)}Tiempo de ejecución: {tiempo:.4f} segundos")
            print(f"\t{chr(10147)}Distancia Total: {algoritmo:.2f}")

        #Busqueda Local
        print(f"Algoritmo de Busqueda Local:")
        print(f"----------------------------")
        #Seleccionamos el algoritmo:
        indice_algoritmo = 1
        nombre_algoritmo = self.algoritmos[indice_algoritmo]
        k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
        maxit = int(self.parametros[4])
        tamentorno = int(self.parametros[5])
        dismentorno=self.parametros[6]
        for i in range(5):
            seed = self.semillas[i]
            print(f"{chr(9635)} Ejecucion numero {i+1} del algoritmo de Busqueda Local sobre el fichero {mapautilizado.nombre}, con la semilla {seed}:")
            start_time = time.perf_counter()
            algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                                tam=mapautilizado.tam, iteraciones=maxit, tamentorno=tamentorno,
                                                dismentorno=dismentorno, )

            end_time = time.perf_counter()
            tiempo = (end_time - start_time)
            print(f"\t{chr(10147)}Tiempo de ejecución: {tiempo:.4f} segundos")
            print(f"\t{chr(10147)}Camino optimo: {algoritmo[0]}")
            print(f"\t{chr(10147)}distancia optima: {algoritmo[1]:.2f}")
        # Tabu
        print(f"Algoritmo de Busqueda Tabu:")
        print(f"----------------------------")
        # Seleccionamos el algoritmo:
        indice_algoritmo = 2
        nombre_algoritmo = self.algoritmos[indice_algoritmo]
        k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
        maxit = int(self.parametros[4])
        tamentorno = int(self.parametros[5])
        dismentorno = float(self.parametros[6])
        porcentajel = float(self.parametros[7])
        iteraciones = int (self.parametros[4])
        tendencia=int(self.parametros[8])
        for i in range(5):
            seed = self.semillas[i]
            print(f"{chr(9635)} Ejecucion numero {i + 1} del algoritmo de Busqueda Tabu sobre el fichero {mapautilizado.nombre}, con la semilla {seed}:")
            start_time = time.perf_counter()
            algoritmo = self.ejecutar_algoritmo(nombre_algoritmo,matriz_distancias=matriz_d,k=k,seed=seed,tam=mapautilizado.tam,iteraciones =iteraciones ,tamentorno=tamentorno,dismentorno=dismentorno,porcentajel=porcentajel,tendencia_tabu=tendencia)
            end_time = time.perf_counter()
            tiempo = (end_time - start_time)
            mGlobal = algoritmo[0]
            mDisGlobal= algoritmo[1]
            print(f"\t{chr(10147)}Tiempo de ejecución: {tiempo:.4f} segundos")
            print(f"\t{chr(10147)}Mejor camino: {mGlobal}")
            print(f"\t{chr(10147)}Distancia del mejor camino: {mDisGlobal:.2f}")

        #Ejecuciones concluidas:
        print(f"Se han concluido todas las ejecuciones sobre el fichero{mapautilizado.nombre}")