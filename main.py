import flet as ft
from database import Database
from views.ingrediente_view import IngredienteView


class AppDoces:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = Database()
        self.configurar_pagina()
        self.renderizar_interface()

    def configurar_pagina(self):
        self.page.title = "Controle de Custos - Doceria"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Ajustes de janela para PC e Mobile
        self.page.window_width = 450
        self.page.window_height = 800
        self.page.padding = 0

    def renderizar_interface(self):
        # Usando o componente de Tabs moderno da versão 0.80.1
        self.tabs = ft.Tabs(
            selected_index=1,
            animation_duration=300,
            expand=True,
            length=2,
            content=ft.Column(
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(
                                label="Receitas",
                                icon=ft.Icons.RESTAURANT_MENU,
                            ),
                            ft.Tab(
                                label="Ingredientes",
                                icon=ft.Icons.KITCHEN,
                            ),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Text("Módulo de Receitas em breve...", size=20),
                                padding=20, alignment=ft.alignment.Alignment.CENTER
                            ),
                            ft.Container(
                                content=IngredienteView(self.db),
                                padding=20
                            ),
                        ]
                    ),
                ]
            ),
        )
        self.page.add(self.tabs)


def main(page: ft.Page):
    AppDoces(page)


if __name__ == "__main__":
    # Para testar no celular:
    # 1. Instale o app 'Flet' na Google Play Store ou App Store
    # 2. Rode este script no PC: flet run --android (ou --ios)
    # OU para abrir no navegador do celular (IP: 192.168.1.39):
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)
    
    ft.app(target=main)