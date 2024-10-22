import os
import importlib
import time
from Ciudad import Ciudad
from Mapa import Mapa

class Configurador:
    def __init__(self):
        self.archivos = []
        self.semillas = []
        self.algoritmos = []
        self.parametros = []

    # Método para leer el archivo de configuración
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
        print(f"Nombre: {miMapa.nombre}")
        print(f"Comentario: {miMapa.comentario}")
        print(f"Tipo: {miMapa.tipo}")
        print(f"Dimensión: {miMapa.tam}")
        print(f"Tipo de peso de arista: {miMapa.edge_type}")

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
                k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
                start_time = time.perf_counter()
                algoritmo = self.ejecutar_algoritmo(nombre_algoritmo,
                                                    matriz_distancias=matriz_d,
                                                    k=k,
                                                    seed=seed,
                                                    tam=mapautilizado.tam)
                end_time = time.perf_counter()
                print(f"Tiempo de ejecución: {end_time - start_time} segundos")
                print(f"Distancia Total: {algoritmo}")

            case "blnueva":
                k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
                maxit = int(self.parametros[4])
                tamentorno = int(self.parametros[5])
                start_time = time.perf_counter()
                dismentorno=self.parametros[6]
                algoritmo = self.ejecutar_algoritmo(nombre_algoritmo,
                                                    matriz_distancias=matriz_d,
                                                    k=k,
                                                    seed=seed,
                                                    tam=mapautilizado.tam,
                                                    iteraciones=maxit,
                                                    tamentorno=tamentorno,
                                                    dismentorno = dismentorno,
                                                    )
                end_time = time.perf_counter()
                tiempo = (end_time - start_time)
                print(f"Tiempo de ejecución: {tiempo} segundos")
                print(f"Camino optimo: {algoritmo[0]}")
                print(f"distancia optima: {algoritmo[1]}")



            case "tabu":
                k = int(self.parametros[3]) if len(self.parametros) > 3 else 5
                maxit = int(self.parametros[4])
                tamentorno = int(self.parametros[5])
                dismentorno = float(self.parametros[6])
                porcentajel = float(self.parametros[7])
                iteraciones = int (self.parametros[4])

                start_time = time.perf_counter()
                algoritmo = self.ejecutar_algoritmo(nombre_algoritmo,matriz_distancias=matriz_d,k=k,seed=seed,tam=mapautilizado.tam,iteraciones =iteraciones ,tamentorno=tamentorno,dismentorno=dismentorno,porcentajel=porcentajel)


                end_time = time.perf_counter()
                mGlobal = algoritmo[0]
                mDisGlobal= algoritmo[1]
                print(f"Tiempo de ejecución: {end_time - start_time} segundos")
                print(f"Mejor camino: {mGlobal}")
                print(f"Distancia del mejor camino: {mDisGlobal}")
            case _:
                print(f"Algoritmo {nombre_algoritmo} no está implementado.")
