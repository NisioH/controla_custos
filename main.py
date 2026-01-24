import flet as ft
from database import Database
from views.ingrediente_view import IngredienteView
from views.receita_view import ReceitaView


class AppDoces:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = Database()
        self.configurar_pagina()
        self.renderizar_interface()

    def configurar_pagina(self):
        self.page.title = "Controle de Custos - Doceria"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 450
        self.page.window_height = 800
        self.page.padding = 0

    def renderizar_interface(self):
        self.tela_receitas = ft.Container(
            content=ReceitaView(self.db),
            visible=False,
            padding=20,
            expand=True
        )

        self.tela_ingredientes = ft.Container(
            content=IngredienteView(self.db),
            visible=True,
            padding=20,
            expand=True
        )


        self.btn_receitas = ft.TextButton(
            "RECEITAS",
            on_click=lambda _: self.mudar_aba(0),
            style=ft.ButtonStyle(color=ft.Colors.WHITE60)
        )
        self.btn_ingredientes = ft.TextButton(
            "INGREDIENTES",
            on_click=lambda _: self.mudar_aba(1),
            style=ft.ButtonStyle(color=ft.Colors.WHITE)  # Destaque inicial
        )

        barra_superior = ft.Container(
            content=ft.Row(
                controls=[self.btn_receitas, self.btn_ingredientes],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=50
            ),
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=15
        )

        self.page.add(
            barra_superior,
            self.tela_receitas,
            self.tela_ingredientes
        )

    def mudar_aba(self, indice):

        self.tela_receitas.visible = (indice == 0)
        self.tela_ingredientes.visible = (indice == 1)

        self.btn_receitas.style.color = ft.Colors.WHITE if indice == 0 else ft.Colors.WHITE60
        self.btn_ingredientes.style.color = ft.Colors.WHITE if indice == 1 else ft.Colors.WHITE60

        if indice == 0:
            self.tela_receitas.content.carregar_dados()

        self.page.update()


def main(page: ft.Page):
    AppDoces(page)


if __name__ == "__main__":
    ft.app(target=main)