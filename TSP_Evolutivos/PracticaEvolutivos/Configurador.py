import os
import importlib
import time
from Ciudad import Ciudad
from Mapa import Mapa
import logging

class Configurador:
    def __init__(self):
        #logging.getLogger().addHandler(logging.NullHandler())
        self.archivos = []
        self.semillas = []
        self.algoritmos = []
        self.parametros = []

        logging.basicConfig(
            level=logging.DEBUG,  # Nivel mínimo que será registrado
            format='%(message)s',  # Formato de los mensajes
            handlers=[
                logging.FileHandler("fichero.log"),  # Guardar logs en un archivo
            ]
        )

    # Método para leer el archivo de configuración
    def leer_archivo_config(self, ruta_config):
        if os.path.isfile(ruta_config):
            with open(ruta_config, "r") as archivo_config:
                seccion_parametros = False
                self.parametros = []
                for linea in archivo_config:
                    linea = linea.strip()

                    # Detecta las secciones del archivo
                    if "Archivos=" in linea:
                        self.archivos = linea.split("=")[1].strip().split()
                    elif "Semillas=" in linea:
                        self.semillas = list(map(int, linea.split("=")[1].strip().split()))
                    elif "Algoritmos=" in linea:
                        self.algoritmos = linea.split("=")[1].strip().split()
                    elif "Parametros de seleccion:" in linea:
                        seccion_parametros = True  # Marca el inicio de los parámetros
                    elif seccion_parametros and ":" in linea:
                        # Extrae el valor después de ":" ignorando el nombre
                        valor = linea.split(":")[1].strip()
                        # Convierte a int si es un número
                        if valor.isdigit():
                            valor = int(valor)
                        # Almacena el valor en la lista de parámetros
                        self.parametros.append(valor)
        else:
            raise FileNotFoundError(f"El archivo de configuración {ruta_config} no existe.")

    # Método para leer el archivo .tsp y procesarlo
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

    # Método para imprimir los detalles del mapa
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

        print("Coordenadas de las ciudades:")
        for ciudad in miMapa.ciudades.values():
            print(f"ID: {ciudad.id}, X: {ciudad.x}, Y: {ciudad.y}")

    # Método para ejecutar dinámicamente un algoritmo
    def ejecutar_algoritmo(self, nombre_algoritmo, *args, **kwargs):
        modulo = importlib.import_module(f"algoritmos.{nombre_algoritmo.lower()}")
        clase_algoritmo = getattr(modulo, nombre_algoritmo)
        instancia = clase_algoritmo(*args, **kwargs)
        return instancia.ejecutar()

    # Método principal que ejecuta la lógica completa
    def ejecutar(self):
        # Rutas de configuración y TSP
        ruta_config = os.path.join('recursos', 'archivosConf', 'ficheroConfiguracion.txt')
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
        indice_archivo = int(self.parametros[0])
        archivo_seleccionado = self.archivos[indice_archivo]
        ruta_archivo_tsp = os.path.join(ruta_tsp, archivo_seleccionado)

        if not os.path.isfile(ruta_archivo_tsp):
            raise FileNotFoundError(f"El archivo TSP {ruta_archivo_tsp} no existe.")

        # Leer y procesar el archivo TSP
        mapautilizado = self.leer_archivo(ruta_archivo_tsp)

        # Mostrar datos del mapa si se desea
        if input('¿Desea mostrar los datos almacenados en la estructura? (Si/No): ').strip().lower() == 'si':
            self.imprimirMapa(mapautilizado)

        # Generar la matriz de distancias
        matriz_d = mapautilizado.generar_matriz_distancias()
        logging.info("Matriz de distancias generada con exito")

        # Preguntar si se desea imprimir la matriz de distancias
        if input('¿Desea imprimir la matriz de distancias? (Si/No): ').strip().lower() == 'si':
            for fila in matriz_d:
                print(' '.join(map(str, fila)))

        # Seleccionar el algoritmo
        indice_algoritmo = int(self.parametros[1])
        nombre_algoritmo = self.algoritmos[indice_algoritmo]

        # Obtener la semilla
        seed = self.semillas[int(self.parametros[2])] if self.semillas else None

        # Selección de algoritmos con switch (Aqui se usa match)
        match nombre_algoritmo.lower():
            case "randomgreedy":
                print(f"Algoritmo Greedy Aleatorio:")
                print(f"---------------------------")
                k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
                start_time = time.perf_counter()
                algoritmo = self.ejecutar_algoritmo(nombre_algoritmo,
                                                    matriz_distancias=matriz_d,
                                                    k=k,
                                                    seed=seed,
                                                    tam=mapautilizado.tam)
                end_time = time.perf_counter()
                tiempo = end_time - start_time
                print(f"\t{chr(223)} Tiempo de ejecución: {tiempo:.4f} segundos")
                print(f"\t{chr(223)} Distancia Total: {algoritmo:.2f}")

            case "busquedalocal":
                print(f"Algoritmo de Busqueda Local:")
                print(f"----------------------------")
                k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
                maxit = int(self.parametros[4])
                tamentorno = int(self.parametros[5])
                dismentorno = self.parametros[6]
                itDismin = self.parametros[7]
                start_time = time.perf_counter()
                algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                                    tam=mapautilizado.tam, iteraciones=maxit, tamentorno=tamentorno,
                                                    dismentorno=dismentorno, itDismin=itDismin)

                end_time = time.perf_counter()
                tiempo = (end_time - start_time)
                print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
                print(f"\t{chr(10147)} Camino optimo: {algoritmo[0]}")
                print(f"\t{chr(10147)} distancia optima: {algoritmo[1]:.2f}")



            case "tabu":
                print(f"Algoritmo de Busqueda Tabu:")
                print(f"---------------------------")
                k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
                tamentorno = int(self.parametros[5])
                dismentorno = float(self.parametros[6])
                porcentajel = float(self.parametros[10])
                iteraciones = int(self.parametros[4])
                itDismin = self.parametros[7]
                tendencia = int(self.parametros[9])
                estanca = int(self.parametros[8])
                start_time = time.perf_counter()
                algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                                    tam=mapautilizado.tam, iteraciones=iteraciones,
                                                    tamentorno=tamentorno, dismentorno=dismentorno,
                                                    porcentajel=porcentajel, tendencia_tabu=tendencia, estanca=estanca,
                                                    itDismin=itDismin)

                end_time = time.perf_counter()
                tiempo = (end_time - start_time)
                mGlobal = algoritmo[0]
                mDisGlobal = algoritmo[1]
                print(f"\t{chr(10147)} Tiempo de ejecución: {tiempo:.4f} segundos")
                print(f"\t{chr(10147)} Mejor camino: {mGlobal}")
                print(f"\t{chr(10147)} Distancia del mejor camino: {mDisGlobal:.2f}")

            case "evolutivogeneracional":
                print(f"Algoritmo evolutivogeneracional:")
                print(f"---------------------------")
                logging.info(f"Algoritmo evolutivogeneracional:")
                logging.info(f"-------------------------------")
                k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
                logging.info(f"\t\tK:\t{k}")
                poblacionmax=int(self.parametros[11])
                logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")
                porcentajealeatorio=int(self.parametros[12])
                logging.info(f"\t\tPorcentaje Aleatorio:\t{porcentajealeatorio}")
                kbest=int(self.parametros[13])
                logging.info(f"\t\tKbest:\t{kbest}")
                kworst=int(self.parametros[14])
                logging.info(f"\t\tkworst:\t{kworst}")
                procruce=int(self.parametros[17])
                logging.info(f"\t\tProcruce:\t{procruce}")
                promut=int(self.parametros[18])
                logging.info(f"\t\tPromut:\t{promut}")
                Evmax = int(self.parametros[17])
                logging.info(f"\t\tEvmax:\t{Evmax}")
                Tmax = int(self.parametros[18])
                logging.info(f"\t\tTmax:\t{Tmax}")
                tipocruce = int(self.parametros[19])
                logging.info(f"\t\tTipocruce:\t{tipocruce}")
                elite = int(self.parametros[20])
                logging.info(f"\t\tElite:\t{elite}")
                start_time = time.perf_counter()
                algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                                    tam=mapautilizado.tam, poblacionmax=poblacionmax, porcentajealeatorio=porcentajealeatorio,kbest=kbest,
                                                    kworst=kworst, procruce=procruce, promut=promut, Evmax=Evmax, Tmax=Tmax, tipocruce=tipocruce,elite=elite)#,num_elites=num_elites)

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

            case "evolutivoestacionario":
                print(f"Algoritmo evolutivoestacionario:")
                print(f"---------------------------")
                logging.info(f"Algoritmo evolutivoestacionario:")
                logging.info(f"-------------------------------")
                k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
                logging.info(f"\t\tK:\t{k}")
                poblacionmax = int(self.parametros[11])
                logging.info(f"\t\tPoblacion Max:\t{poblacionmax}")
                porcentajealeatorio = int(self.parametros[12])
                logging.info(f"\t\tPorcentaje aleatorio:\t{porcentajealeatorio}")
                kbest = int(self.parametros[13])
                logging.info(f"\t\tKbest:\t{kbest}")
                kworst = int(self.parametros[14])
                logging.info(f"\t\tkworst:\t{kworst}")
                promut = int(self.parametros[18])
                logging.info(f"\t\tPromut:\t{promut}")
                Evmax = int(self.parametros[17])
                logging.info(f"\t\tEvmax:\t{Evmax}")
                Tmax = int(self.parametros[18])
                logging.info(f"\t\tTmax:\t{Tmax}")
                tipocruce = int(self.parametros[19])
                logging.info(f"\t\tTipocruce:\t{tipocruce}")
                start_time = time.perf_counter()
                algoritmo = self.ejecutar_algoritmo(nombre_algoritmo, matriz_distancias=matriz_d, k=k, seed=seed,
                                                    tam=mapautilizado.tam, poblacionmax=poblacionmax,
                                                    porcentajealeatorio=porcentajealeatorio, kbest=kbest,
                                                    kworst=kworst,promut=promut, Evmax=Evmax,
                                                    Tmax=Tmax,tipocruce=tipocruce)

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



            case _:
                print(f"Algoritmo {nombre_algoritmo} no está implementado.")
