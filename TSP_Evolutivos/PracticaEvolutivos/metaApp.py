import os
import flet as ft
from flet_core import TextStyle

import widgetConfigurador


def main(page: ft.Page):
    # Configuración del tema
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary='#1C2026',
            on_primary='#A4A5A6',
            secondary='#2D3540',
            on_secondary='#A4A5A6',
            tertiary='#A4A5A6',
            on_tertiary='#1C2026',
        ),
    )
    page.title = "MetaTSP"
    page.window.width = 400
    page.window.height = 600
    page.bgcolor = ft.colors.SECONDARY

    # AppBar personalizada
    page.appbar = ft.AppBar(
        title=ft.Text("Metaheurísticas", style=TextStyle(size=30, color=ft.colors.WHITE)),
        center_title=True,
        bgcolor=ft.colors.PRIMARY,
    )

    # Función de navegación
    def navegar_a_parametros(algoritmo):
        # Cambiar a la vista correspondiente basada en el algoritmo seleccionado
        match algoritmo:
            case "Random Greedy":
                page.views.append(widgetConfigurador.randomGreedyView(page))
            case "Búsqueda Local":
                page.views.append(widgetConfigurador.busquedaLocalView(page))
            case "Búsqueda Tabú":
                page.views.append(widgetConfigurador.busquedaTabuView(page))
            case _:
                print("Algoritmo no soportado")
        page.update()

    # Elementos de la vista principal
    ruta_tsp = os.path.join('recursos', 'archivosTSP')
    desplegable_archivo = widgetConfigurador.listar_archivos(ruta_tsp)
    desplegable_semilla = widgetConfigurador.opcionSemilla()
    desplegable_algoritmo = widgetConfigurador.opcionAlgoritmo()
    botonParametros = widgetConfigurador.botonMostrarParametros(desplegable_algoritmo, navegar_a_parametros)

    # Inicialmente desactivar el botón
    botonParametros.disabled = True

    # Función para comprobar si todos los desplegables tienen un valor seleccionado
    def comprobar_seleccion(event=None):
        if (desplegable_archivo.value and
            desplegable_semilla.value and
            desplegable_algoritmo.value):
            botonParametros.disabled = False
        else:
            botonParametros.disabled = True
        # Refrescar la interfaz
        page.update()

    # Añadir eventos a los desplegables para actualizar el estado
    desplegable_archivo.on_change = comprobar_seleccion
    desplegable_semilla.on_change = comprobar_seleccion
    desplegable_algoritmo.on_change = comprobar_seleccion

    # Contenido de la vista principal
    page.add(
        ft.Column([
            ft.Text("Seleccione el fichero a procesar:", size=20),
            desplegable_archivo,
            ft.Text("Seleccione la semilla a emplear:", size=20),
            desplegable_semilla,
            ft.Text("Seleccione el algoritmo a aplicar:", size=20),
            desplegable_algoritmo,
            ft.Divider(height=9, thickness=1, color=ft.colors.SECONDARY),
            botonParametros,
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    )


ft.app(target=main)
