import os
import flet as ft
from flet_core import TextStyle, MainAxisAlignment, Alignment


def main(page: ft.Page):
    # Funciones Auxiliares:
    def listar_archivos(directorio):
        if os.path.exists(directorio) and os.path.isdir(directorio):
            archivos = os.listdir(directorio)
            opciones = [ft.dropdown.Option(archivo) for archivo in archivos]  # Crear opciones dinámicamente
            dropdown = ft.Dropdown(
                width=300,
                border_radius=10,
                text_style=TextStyle(size=18, italic=True),
                filled=True,
                fill_color=ft.colors.TERTIARY,
                options=opciones,  # Asignar las opciones generadas
            )
            return dropdown
        else:
            print(f"El directorio '{directorio}' no existe o no es un directorio.")
            return None

    # Configuración del tema
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary='#202B4B',
            secondary='#333C58',
            tertiary='#6A738F',
        ),
    )
    page.bgcolor = ft.colors.SECONDARY

    # AppBar personalizada
    page.appbar = ft.AppBar(
        title=ft.Text("Metaheurísticas", style=TextStyle(size=30, color=ft.colors.WHITE)),
        center_title=True,
        bgcolor=ft.colors.PRIMARY,
    )

    # Títulos y elementos visuales
    header = ft.Text("Configuración de Parámetros", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)

    # Selección de algoritmo
    texto_algoritmo = ft.Text(
        "Seleccione el algoritmo que desee ejecutar:",
        style=TextStyle(size=20, color=ft.colors.WHITE),
    )
    desplegable_algoritmo = ft.Dropdown(
        width=300,
        border_radius=10,
        text_style=TextStyle(size=18, italic=True),
        filled=True,
        fill_color=ft.colors.TERTIARY,
        options=[
            ft.dropdown.Option("Random Greedy"),
            ft.dropdown.Option("Búsqueda Local"),
            ft.dropdown.Option("Búsqueda Tabú"),
            ft.dropdown.Option("Evolutivo Generacional"),
            ft.dropdown.Option("Evolutivo Estacionario"),
        ],
    )

    # Selección de archivo
    texto_archivo = ft.Text(
        "Seleccione el archivo que desea procesar:",
        style=TextStyle(size=20, color=ft.colors.WHITE),
    )
    ruta_tsp = os.path.join('recursos', 'archivosTSP')
    desplegable_archivo = listar_archivos(ruta_tsp)

    # Selección de semilla
    texto_semilla = ft.Text(
        "Seleccione la semilla:",
        style=TextStyle(size=20, color=ft.colors.WHITE),
    )
    desplegable_semilla = ft.Dropdown(
        width=300,
        border_radius=10,
        text_style=TextStyle(size=18, italic=True),
        filled=True,
        fill_color=ft.colors.TERTIARY,
        options=[
            ft.dropdown.Option("77693013"),
            ft.dropdown.Option("76930137"),
            ft.dropdown.Option("69301377"),
            ft.dropdown.Option("93013776"),
            ft.dropdown.Option("21025743"),
        ],
    )

    # Botón de opciones
    def mostrar_parametros(event):
        #Mostramos ahora una columna u otra en funcion del algoritmo seleccionado
        print(desplegable_algoritmo.value)
        if desplegable_algoritmo.value == "Evolutivo Generacional":
            vistaParametros = ft.SafeArea(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("K"),
                            ft.TextField("HolaMundo")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    width=600,
                    bgcolor=ft.colors.PRIMARY,
                    padding=30,
                    border_radius=20,

                ),
            )
            page.controls.clear()
            page.add(vistaParametros)
            page.update()
        else:
            print("Aquiestou")

    boton_seleccion = ft.ElevatedButton(
        text="Configurar Parámetros",
        on_click=mostrar_parametros,
        icon="SETTINGS",
        icon_color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            text_style=TextStyle(size=20, color=ft.colors.WHITE),
            bgcolor=ft.colors.TERTIARY,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=5),
            padding=20,
        ),
    )

    # Agregar elementos al diseño
    page.add(
        ft.SafeArea(
            ft.Container(
                content=ft.Column(
                    [
                        header,
                        texto_algoritmo,
                        desplegable_algoritmo,
                        texto_archivo,
                        desplegable_archivo,
                        texto_semilla,
                        desplegable_semilla,
                        boton_seleccion,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                width=600,
                bgcolor=ft.colors.PRIMARY,
                padding=30,
                border_radius=20,
            ),
        )
    )




ft.app(target=main)
