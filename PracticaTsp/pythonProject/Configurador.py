import os
from Mapa import Mapa  # Asumo que tienes esta clase creada
from Ciudad import Ciudad  # Asumo que tienes esta clase creada

class Configurador:
    def __init__(self):
        self.archivos = []
        self.semillas = []
        self.algoritmos = []
        self.otro_parametro = None

    ## Función para leer el archivo de configuración
    def leer_configuracion(self, ruta_config):
        if not os.path.exists(ruta_config):
            print(f"El archivo de configuración {ruta_config} no existe.")
            return False

        with open(ruta_config, "r") as archivo_config:
            for linea in archivo_config:
                linea = linea.strip()
                if "Archivos=" in linea:
                    self.archivos = linea.split("=")[1].strip().split()
                elif "Semillas=" in linea:
                    self.semillas = list(map(int, linea.split("=")[1].strip().split()))
                elif "Algoritmos=" in linea:
                    self.algoritmos = linea.split("=")[1].strip().split()
                elif "otroparametro=" in linea:
                    self.otro_parametro = int(linea.split("=")[1].strip())

        return True

    ## Función para que el usuario seleccione uno de los archivos listados en la configuración
    def seleccionar_archivo(self):
        if not self.archivos:
            print("No se han encontrado archivos en la configuración.")
            return None

        print("Archivos disponibles en la configuración:")
        for i, archivo in enumerate(self.archivos):
            print(f"{i + 1}. {archivo}")

        while True:
            try:
                seleccion = int(input("Seleccione el número del archivo que desea procesar: "))
                if 1 <= seleccion <= len(self.archivos):
                    return self.archivos[seleccion - 1]
                else:
                    print("Por favor, seleccione un número válido.")
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")

    ## Función para que el usuario seleccione el algoritmo y la semilla deseada
    def seleccionar_algoritmo_y_semilla(self):
        if not self.algoritmos:
            print("No se han encontrado algoritmos en la configuración.")
            return None, None

        print("Algoritmos disponibles:")
        for i, algoritmo in enumerate(self.algoritmos):
            print(f"{i + 1}. {algoritmo}")

        while True:
            try:
                seleccion_algoritmo = int(input("Seleccione el número del algoritmo que desea ejecutar: "))
                if 1 <= seleccion_algoritmo <= len(self.algoritmos):
                    algoritmo_seleccionado = self.algoritmos[seleccion_algoritmo - 1]
                    break
                else:
                    print("Por favor, seleccione un número válido.")
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")

        print("Semillas disponibles:")
        for i, semilla in enumerate(self.semillas):
            print(f"{i + 1}. {semilla}")

        while True:
            try:
                seleccion_semilla = int(input("Seleccione el número de la semilla que desea usar: "))
                if 1 <= seleccion_semilla <= len(self.semillas):
                    semilla_seleccionada = self.semillas[seleccion_semilla - 1]
                    return algoritmo_seleccionado, semilla_seleccionada
                else:
                    print("Por favor, seleccione un número válido.")
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")

    ## Función para leer el archivo de ciudades en formato TSP
    def leer_archivo(self, archivo):
        miMapa = Mapa()  # Creamos un objeto Mapa
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
        print(f"Archivo {archivo} procesado con éxito.")
        return miMapa

    ## Función principal para ejecutar todo el flujo
    def ejecutar(self):
        # Leer la configuración desde el archivo config_1.txt
        ruta_config = os.path.join(os.getcwd(), 'archivosConf', 'config_1.txt')
        if not self.leer_configuracion(ruta_config):
            return

        # Seleccionar un archivo de los listados en la configuración
        archivo_seleccionado = self.seleccionar_archivo()
        if not archivo_seleccionado:
            print("No se seleccionó un archivo válido.")
            return

        # Leer el archivo de ciudades (TSP)
        ruta_archivo = os.path.join(os.getcwd(), 'recursos', archivo_seleccionado)
        mapa = self.leer_archivo(ruta_archivo)

        # Seleccionar algoritmo y semilla
        algoritmo, semilla = self.seleccionar_algoritmo_y_semilla()
        if not algoritmo or not semilla:
            print("No se seleccionó un algoritmo o semilla válidos.")
            return

        print(f"Ejecutando {algoritmo} con semilla {semilla} y otro parámetro {self.otro_parametro}.")
        # Aquí ejecutarías el algoritmo seleccionado. Ejemplo:
        if algoritmo == "RandomGreedy":
            resultado = mapa.randomGreedy(self.otro_parametro, semilla)
            print(f"Resultado del algoritmo {algoritmo}: {resultado}")
        elif algoritmo == "Busquedalocal":
            # Lógica para BusquedaLocal
            pass

