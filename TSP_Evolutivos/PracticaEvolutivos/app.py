#flet run -d  main.py

import os
import flet as ft
from flet_core import TextStyle, Alignment, ButtonStyle


def main(page: ft.Page):
    #Funciones Auxiliares:
    def listar_archivos(directorio):
        if os.path.exists(directorio) and os.path.isdir(directorio):
            archivos = os.listdir(directorio)
            dropdowns = []
            for archivo in archivos:
                dropdown = ft.Dropdown(
                    width=220,
                    border_radius=10,
                    text_style=TextStyle(size=18, italic=True),
                    filled=True,
                    fill_color=ft.colors.TERTIARY,
                    options=[
                        ft.dropdown.Option(archivo)  # Cada archivo será una opción
                    ],
                )
                dropdowns.append(dropdown)
            return dropdowns
        else:
            print(f"El directorio '{directorio}' no existe o no es un directorio.")
            return []
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary='#202B4B',
            #on_primary=ft.colors.YELLOW,
            #primary_container=ft.colors.GREEN_200,
            secondary='#333C58',
            #on_secondary=ft.colors.YELLOW,
            #secondary_container=ft.colors.GREEN_200,
            tertiary='#6A738F',
            #on_secondary_container=ft.colors.YELLOW,

        ),
    )
    page.bgcolor=ft.colors.SECONDARY

    page.appbar = ft.AppBar(
        title=ft.Text("Metaheuristicas",style=TextStyle(size=35),),
        center_title=True,
        bgcolor=ft.colors.PRIMARY,

    )
    #Seleccionar algoritmo:
    texto_algoritmo = ft.Text("Seleccione el algoritmo que desee ejecutar:",style=TextStyle(size=20),)
    desplegable_algoritmo = ft.Dropdown(
        width=220,
        border_radius=10,
        text_style=TextStyle(size=18,italic=True),
        filled=True,
        fill_color=ft.colors.TERTIARY,
        options=[
            ft.dropdown.Option("Random Greedy"),
            ft.dropdown.Option("Busqueda Local"),
            ft.dropdown.Option("Busqueda Tabu"),
            ft.dropdown.Option("Evolutivo Generacional"),
            ft.dropdown.Option("Evolutivo Estacionario"),
        ],
    )
    #Seleccionar Archivo:
    texto_archivo = ft.Text("Seleccione el archivo que desea procesar:", style=TextStyle(size=20), )
    desplegable_archivo = listar_archivos("recursos/archivosConf")
    #Selecciona Semilla:
    texto_semilla = ft.Text("Selecciona la semilla:", style=TextStyle(size=20), )
    desplegable_semilla = ft.Dropdown(
        width=220,
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
    #Boton de opciones
    # Función para manejar el evento del botón
    def mostrar_parametros(event):
        print("Botón presionado")

    boton_seleccion= ft.FilledButton(text="Conficurar Parametros", on_click=mostrar_parametros, icon="SETTINGS", icon_color=ft.colors.WHITE, style=ft.ButtonStyle(
                bgcolor=ft.colors.PRIMARY,color=ft.colors.WHITE,shape=ft.RoundedRectangleBorder(radius=5)
            ),)
    page.add(
        ft.SafeArea(
            ft.Row([
                ft.Column([
                    texto_algoritmo, desplegable_algoritmo, texto_archivo, desplegable_archivo, texto_semilla,
                    desplegable_semilla,boton_seleccion
                ],horizontal_alignment=ft.CrossAxisAlignment.START,expand=True),
                ft.Column([
                    texto_algoritmo, desplegable_algoritmo, texto_archivo, desplegable_archivo, texto_semilla,
                    desplegable_semilla
                ],horizontal_alignment=ft.CrossAxisAlignment.END,expand=True),
            ],   expand=True, alignment=ft.MainAxisAlignment.CENTER),
        )
    )

ft.app(main)