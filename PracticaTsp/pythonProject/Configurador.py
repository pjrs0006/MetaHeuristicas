import os
from Mapa import Mapa  # Asumo que tienes esta clase creada
from Ciudad import Ciudad  # Asumo que tienes esta clase creada

## \file main.py
#  \brief Este archivo contiene la lógica principal para procesar un conjunto de ciudades desde un archivo, generar la matriz de distancias y ejecutar un algoritmo greedy.

import os
import importlib
from Ciudad import Ciudad
from Mapa import Mapa

class Configurador:
    def __init__(self):
        self.archivos = []
        self.semillas = []
        self.algoritmos = []
        self.parametros = []

    def leer_archivo_config(self, ruta_config):
        if os.path.isfile(ruta_config):
            # Abre el archivo y procesa cada línea
            with open(ruta_config, "r") as archivo_config:
                for linea in archivo_config:
                    linea = linea.strip()  # Elimina espacios en blanco alrededor de la línea
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

    def leer_archivo(self, archivo):
        # Creamos un objeto Mapa
        miMapa = Mapa()
        # Bandera para indicar si hemos llegado a la sección de coordenadas
        seccionCoordenadas = False

        # Abrimos el archivo en modo lectura
        with open(archivo, "r") as archivo_tsp:
            for linea in archivo_tsp:
                linea = linea.strip()

                # Detectar cuando empieza la sección de coordenadas
                if linea == "NODE_COORD_SECTION":
                    seccionCoordenadas = True
                    continue

                # Detectar el final del archivo
                if linea == "EOF":
                    break

                # Procesar las líneas de la cabecera antes de la sección de coordenadas
                if not seccionCoordenadas:
                    if ":" in linea:
                        clave, valor = linea.split(":", 1)
                        clave = clave.strip().upper()
                        valor = valor.strip()

                        # Asignar los valores correspondientes a los atributos de Mapa
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
                    # Procesar las coordenadas de las ciudades
                    partes = linea.split()
                    if len(partes) == 3:
                        id_nodo = int(partes[0])
                        x = float(partes[1])
                        y = float(partes[2])
                        # Crear una nueva instancia de Ciudad
                        ciudad = Ciudad(id_nodo, x, y)
                        # Añadir la ciudad al objeto Mapa
                        miMapa.ciudades[id_nodo] = ciudad
        print("Archivo procesado con éxito.")
        return miMapa

    def imprimirMapa(self, miMapa):
        # Imprimir la cabecera del mapa
        print(f"Nombre: {miMapa.nombre}")
        print(f"Comentario: {miMapa.comentario}")
        print(f"Tipo: {miMapa.tipo}")
        print(f"Dimensión: {miMapa.tam}")
        print(f"Tipo de peso de arista: {miMapa.edge_type}")

        # Imprimir las coordenadas de las ciudades
        print("Coordenadas de las ciudades:")
        for ciudad in miMapa.ciudades.values():
            print(f"ID: {ciudad.id}, X: {ciudad.x}, Y: {ciudad.y}")

    def ejecutar_algoritmo(self, nombre_algoritmo, *args, **kwargs):
        try:
            # Asumiendo que cada algoritmo está en un módulo separado dentro de la carpeta 'algoritmos'
            modulo = importlib.import_module(f"algoritmos.{nombre_algoritmo.lower()}")
            clase_algoritmo = getattr(modulo, nombre_algoritmo)
            instancia = clase_algoritmo(*args, **kwargs)
            return instancia.ejecutar()
        except (ModuleNotFoundError, AttributeError) as e:
            raise ImportError(f"El algoritmo {nombre_algoritmo} no se encontró o está mal definido.") from e

    ## \brief Función principal del programa.
    #
    #  Esta función coordina todo el proceso: desde listar archivos, permitir al usuario seleccionar uno, leer el archivo, mostrar el mapa, generar la matriz de distancias y ejecutar el algoritmo seleccionado.
    #
    def ejecutar(self):
        # Rutas de configuración y TSP
        ruta_config = os.path.join('recursos', 'archivosConf', 'Config_1.txt')
        ruta_tsp = os.path.join('recursos', 'archivosTSP')

        # Leer archivo de configuración
        self.leer_archivo_config(ruta_config)

        # Validar que haya archivos y algoritmos configurados
        if not self.archivos:
            raise ValueError("No se han especificado archivos en la configuración.")
        if not self.algoritmos:
            raise ValueError("No se han especificado algoritmos en la configuración.")
        if not self.parametros or len(self.parametros) < 2:
            raise ValueError("Los parámetros de configuración son insuficientes.")

        # Obtener el archivo TSP a utilizar
        indice_archivo = int(self.parametros[0])
        if indice_archivo < 0 or indice_archivo >= len(self.archivos):
            raise IndexError(f"Índice de archivo {indice_archivo} fuera de rango.")
        archivo_seleccionado = self.archivos[indice_archivo]
        ruta_archivo_tsp = os.path.join(ruta_tsp, archivo_seleccionado)

        if not os.path.isfile(ruta_archivo_tsp):
            raise FileNotFoundError(f"El archivo TSP {ruta_archivo_tsp} no existe.")

        # Leer y procesar el archivo TSP
        mapautilizado = self.leer_archivo(ruta_archivo_tsp)

        # Preguntar si se deben mostrar los datos del mapa
        print('¿Desea mostrar los datos almacenados en la estructura?')
        mostrarResultados = input('Si/No: ').strip().lower()
        if mostrarResultados == 'si':
            self.imprimirMapa(mapautilizado)
        else:
            print('Perfecto, no se imprimirán los datos almacenados en el mapa.')

        # Generar la matriz de distancias
        matriz_d = mapautilizado.generar_matriz_distancias()

        # Preguntar si se desea imprimir la matriz de distancias
        print('¿Desea imprimir la matriz de distancias?')
        mostrarMatriz = input('Si/No: ').strip().lower()
        if mostrarMatriz == 'si':
            print('Mostrando la matriz de distancias:')
            for fila in matriz_d:
                print(' '.join(map(str, fila)))

        # Seleccionar el algoritmo a ejecutar
        indice_algoritmo = int(self.parametros[1])
        if indice_algoritmo < 0 or indice_algoritmo >= len(self.algoritmos):
            raise IndexError(f"Índice de algoritmo {indice_algoritmo} fuera de rango.")
        nombre_algoritmo = self.algoritmos[indice_algoritmo]

        # Obtener la semilla correspondiente
        if self.semillas:
            seed = self.semillas[indice_archivo % len(self.semillas)]  # Seleccionar semilla basada en el índice del archivo
        else:
            seed = None

        # Ejecutar el algoritmo seleccionado
        if nombre_algoritmo.lower() == "randomgreedy":
            # Obtener 'k' de parámetros o usar un valor por defecto
            k = int(self.parametros[2]) if len(self.parametros) > 2 else 2
            algoritmo = self.ejecutar_algoritmo(
                nombre_algoritmo,
                matriz_distancias=matriz_d,
                k=k,
                seed=seed
            )
            distancia_total, ruta = algoritmo
        else:
            print(f"Algoritmo {nombre_algoritmo} no está implementado.")

