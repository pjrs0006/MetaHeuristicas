import os
import flet as ft
import Configurador

from flet_core import TextStyle, MainAxisAlignment, CrossAxisAlignment, KeyboardType


# Funcion que lista todos los archivos existentes en un directorio y los pasa a un DropDown
def listar_archivos(directorio):
    if os.path.exists(directorio) and os.path.isdir(directorio):
        archivos = os.listdir(directorio)
        opciones = [ft.dropdown.Option(archivo) for archivo in archivos]  # Crear opciones dinámicamente
        dropdown = ft.Dropdown(
            width=300,
            border_radius=10,
            text_style=TextStyle(size=18, italic=True, color=ft.colors.ON_TERTIARY),
            filled=True,
            fill_color=ft.colors.TERTIARY,
            bgcolor=ft.colors.TERTIARY,
            # Asignar las opciones generadas
            options=opciones,
            icon_enabled_color=ft.colors.ON_TERTIARY,
        )
        return dropdown
    else:
        print(f"El directorio '{directorio}' no existe o no es un directorio.")
        return None

# Funcion que devuelve el dropdown de semilla:
def opcionSemilla():
    return ft.Dropdown(
        width=300,
        border_radius=10,
        text_style=TextStyle(size=18, italic=True, color=ft.colors.ON_TERTIARY),
        filled=True,
        fill_color=ft.colors.TERTIARY,
        bgcolor=ft.colors.TERTIARY,
        icon_enabled_color=ft.colors.ON_TERTIARY,
        options=[
            ft.dropdown.Option("77693013"),
            ft.dropdown.Option("76930137"),
            ft.dropdown.Option("69301377"),
            ft.dropdown.Option("93013776"),
            ft.dropdown.Option("21025743"),
        ],
    )

def opcionAlgoritmo():
    return  ft.Dropdown(
        width=300,
        border_radius=10,
        text_style=TextStyle(size=18, italic=True, color=ft.colors.ON_TERTIARY),
        filled=True,
        fill_color=ft.colors.TERTIARY,
        bgcolor=ft.colors.TERTIARY,
        icon_enabled_color=ft.colors.ON_TERTIARY,
        options=[
            ft.dropdown.Option("Random Greedy"),
            ft.dropdown.Option("Búsqueda Local"),
            ft.dropdown.Option("Búsqueda Tabú"),
            ft.dropdown.Option("Evolutivo Generacional"),
            ft.dropdown.Option("Evolutivo Estacionario"),
        ],
    )

# Vista de Random Greedy
def randomGreedyView(archivo,semilla):
        ft.SafeArea(
            ft.Container(
                ft.Column([
                    ft.Text("Ventana (K):", size=20),
                    ft.TextField("5")
                ], alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER),
                alignment=ft.alignment.top_center,
            ),
            expand=True,
        )
# Funcion que muestra los parametros en funcion del algoritmo seleccionado
def mostrar_parametros(dropdownAlgoritmo):
    algoritmo = dropdownAlgoritmo.value
    print(algoritmo)
    # Segun el algoritmo lanzamos una vista u otra:
    match algoritmo:
        case "Random Greedy":
            print("Mostrando opciones de Random Greedy")
        case _:
            print("Opción no válida")
# VISTAS ALGORITMOS
#Funciones para la ejecucion:
ruta_tsp = os.path.join('recursos', 'archivosTSP')
#ruta_archivo_tsp = os.path.join(ruta_tsp, )

# Vista de Random Greedy
def randomGreedyView(page):
    return ft.View(
        "/random_greedy",
        bgcolor=ft.colors.SECONDARY,
        controls=[
            ft.AppBar(
                title=ft.Text("Random Greedy", style=TextStyle(size=30, color=ft.colors.WHITE)),
                bgcolor=ft.colors.PRIMARY,
                center_title=True,
                automatically_imply_leading=False
            ),
            ft.SafeArea(
                ft.Column([
                    ft.Text("Configuración para Random Greedy", size=20),
                    ft.Text("Ventana (K):", size=18),
                    ft.TextField(width=300, value="5",bgcolor=ft.colors.TERTIARY,color=ft.colors.PRIMARY,keyboard_type=KeyboardType.NUMBER),
                    ft.ElevatedButton(
                        text="Ejecutar Algoritmo",
                        on_click=lambda e: page.go("/"),
                        icon=ft.icons.TRAVEL_EXPLORE,
                        icon_color = ft.colors.WHITE,
                        style = ft.ButtonStyle(
                        text_style=TextStyle(size=20, color=ft.colors.WHITE),
                        bgcolor=ft.colors.PRIMARY,
                        color=ft.colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=5),
                        padding=10,
                    ),),
                    ft.TextField(width=300, value="5", bgcolor=ft.colors.TERTIARY, color=ft.colors.PRIMARY,),
                ], alignment=ft.MainAxisAlignment.CENTER,),
            )
        ],
    )

# Vista de Búsqueda Local
def busquedaLocalView(page):
    return ft.View(
        "/busqueda_local",
        controls=[
            ft.AppBar(
                title=ft.Text("Búsqueda Local", style=ft.TextStyle(size=25, color=ft.colors.WHITE)),
                bgcolor=ft.colors.PRIMARY,
                center_title=True,
                actions=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda e: page.go("/")
                    )
                ],
            ),
            ft.Column([
                ft.Text("Configuración para Búsqueda Local", size=20),
                ft.TextField(label="Iteraciones Máximas", width=300),
                ft.ElevatedButton(
                    text="Aceptar",
                    on_click=lambda e: page.go("/")
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ],
    )

# Vista de Búsqueda Tabú
def busquedaTabuView(page):
    return ft.View(
        "/busqueda_tabu",
        controls=[
            ft.AppBar(
                title=ft.Text("Búsqueda Tabú", style=ft.TextStyle(size=25, color=ft.colors.WHITE)),
                bgcolor=ft.colors.PRIMARY,
                center_title=True,
                actions=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda e: page.go("/")
                    )
                ],
            ),
            ft.Column([
                ft.Text("Configuración para Búsqueda Tabú", size=20),
                ft.TextField(label="Tamaño de la Lista Tabú", width=300),
                ft.ElevatedButton(
                    text="Aceptar",
                    on_click=lambda e: page.go("/")
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ],
    )

# Boton para pasar a la vista de introduccion de parametros
def botonMostrarParametros(algoritmo_dropdown, navegar_a_parametros):
    return ft.ElevatedButton(
        text="Configurar Parámetros",
        on_click=lambda e: navegar_a_parametros(algoritmo_dropdown.value),
        icon="SETTINGS",
        icon_color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            text_style=TextStyle(size=20, color=ft.colors.WHITE),
            bgcolor=ft.colors.PRIMARY,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=5),
            padding=20,
        ),
    )
