import flet as ft
from database import Database
from views.dashboard_view import DashboardView
from views.ingrediente_view import IngredienteView
from views.receita_view import ReceitaView


class AppDoces:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = Database()
        self.configurar_pagina()
        self.renderizar_interface()

    def configurar_pagina(self):
        self.page.title = "Custo Doces - Gestão Profissional"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.width = 450
        self.page.window.height = 800
        self.page.padding = 0

        self.page.go_home = lambda: self.mudar_aba(0)

    def renderizar_interface(self):
        self.view_dashboard = DashboardView(self.db, ao_editar=self.abrir_edicao_receita)
        self.view_receita = ReceitaView(self.db)
        self.view_ingrediente = IngredienteView(self.db)

        self.tela_dashboard = ft.Container(content=self.view_dashboard, visible=True, expand=True, padding=20)
        self.tela_receitas = ft.Container(content=self.view_receita, visible=False, expand=True, padding=20)
        self.tela_ingredientes = ft.Container(content=self.view_ingrediente, visible=False, expand=True, padding=20)

        self.btn_inicio = ft.TextButton(
            "Início",
            on_click=lambda _: self.mudar_aba(0),
            style=ft.ButtonStyle(color=ft.Colors.WHITE)
        )
        self.btn_receitas = ft.TextButton(
            "Nova Receita",
            on_click=lambda _: self.mudar_aba(1),
            style=ft.ButtonStyle(color=ft.Colors.WHITE60)
        )
        self.btn_ingredientes = ft.TextButton(
            "Ingredientes",
            on_click=lambda _: self.mudar_aba(2),
            style=ft.ButtonStyle(color=ft.Colors.WHITE60)
        )

        barra_superior = ft.Container(
            content=ft.Row(
                [self.btn_inicio, self.btn_receitas, self.btn_ingredientes],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=10
        )

        self.page.add(
            barra_superior,
            self.tela_dashboard,
            self.tela_receitas,
            self.tela_ingredientes
        )

        self.view_dashboard.carregar_dados()

    def mudar_aba(self, indice):
        self.tela_dashboard.visible = (indice == 0)
        self.tela_receitas.visible = (indice == 1)
        self.tela_ingredientes.visible = (indice == 2)

        if indice == 1 and not self.tela_receitas.visible:
            self.view_receita.id_receita_atual = None
            #self.view_receita.limpar_campos() # Caso tenha essa função

        self.btn_inicio.style.color = ft.Colors.WHITE if indice == 0 else ft.Colors.WHITE60
        self.btn_receitas.style.color = ft.Colors.WHITE if indice == 1 else ft.Colors.WHITE60
        self.btn_ingredientes.style.color = ft.Colors.WHITE if indice == 2 else ft.Colors.WHITE60

        if indice == 0: self.view_dashboard.carregar_dados()
        if indice == 1: self.view_receita.carregar_dados()
        if indice == 2: self.view_ingrediente.carregar_dados()

        self.page.update()

    def abrir_edicao_receita(self, dados_receita):
        """Função chamada quando clicamos em uma receita no Dashboard"""
        self.mudar_aba(1)
        self.view_receita.preparar_edicao(dados_receita)


def main(page: ft.Page):
    AppDoces(page)


if __name__ == "__main__":
    ft.app(target=main)