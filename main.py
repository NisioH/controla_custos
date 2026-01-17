# import flet as ft
# from database import Database
# from views.ingrediente_view import IngredienteView
# from views.receita_view import ReceitaView
#
#
# class AppDoces:
#     def __init__(self, page: ft.Page):
#         self.page = page
#         self.db = Database()
#         self.configurar_pagina()
#         self.renderizar_interface()
#
#     def configurar_pagina(self):
#         self.page.title = "Controle de Custos - Doceria"
#         self.page.theme_mode = ft.ThemeMode.DARK
#
#         # Ajustes de janela para PC e Mobile
#         self.page.window_width = 450
#         self.page.window_height = 800
#         self.page.padding = 0
#
#
#
#     def renderizar_interface(self):
#         # Usando o componente de Tabs moderno da versão 0.80.1
#         self.tabs = ft.Tabs(
#             selected_index=1,
#             animation_duration=300,
#             expand=True,
#             length=2,
#             content=ft.Column(
#                 controls=[
#                     ft.TabBar(
#                         tabs=[
#                             ft.Tab(
#                                 label="Receitas",
#                                 icon=ft.Icons.RESTAURANT_MENU,
#                             ),
#                             ft.Tab(
#                                 label="Ingredientes",
#                                 icon=ft.Icons.KITCHEN,
#                             ),
#                         ]
#                     ),
#                     ft.TabBarView(
#                         expand=True,
#                         controls=[
#                             ft.Container(
#                                 content=ReceitaView(self.db),
#                                 padding=20,
#                             ),
#                             ft.Container(
#                                 content=IngredienteView(self.db),
#                                 padding=20
#                             ),
#                         ]
#                     ),
#                 ]
#             ),
#         )
#         self.page.add(self.tabs)
#
#
# def main(page: ft.Page):
#     AppDoces(page)
#
#
# if __name__ == "__main__":
#     # Para testar no celular:
#     # 1. Instale o app 'Flet' na Google Play Store ou App Store
#     # 2. Rode este script no PC: flet run --android (ou --ios)
#     # OU para abrir no navegador do celular (IP: 192.168.1.39):
#     # ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)
#
#     ft.app(target=main)


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
        # 1. Criamos as telas
        self.tela_receitas = ft.Container(
            content=ReceitaView(self.db),
            visible=False,  # Começa escondida
            padding=20,
            expand=True
        )

        self.tela_ingredientes = ft.Container(
            content=IngredienteView(self.db),
            visible=True,  # Começa visível
            padding=20,
            expand=True
        )

        # 2. Criamos botões simples que funcionam como abas
        # Isso evita o erro de 'selected_index' ou 'content' do TabBar
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

        # 3. Barra Superior Customizada
        barra_superior = ft.Container(
            content=ft.Row(
                controls=[self.btn_receitas, self.btn_ingredientes],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=50
            ),
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=15
        )

        # 4. Adiciona tudo à página
        self.page.add(
            barra_superior,
            self.tela_receitas,
            self.tela_ingredientes
        )

    def mudar_aba(self, indice):
        # Lógica de visibilidade das telas
        self.tela_receitas.visible = (indice == 0)
        self.tela_ingredientes.visible = (indice == 1)

        # Lógica visual dos botões
        self.btn_receitas.style.color = ft.Colors.WHITE if indice == 0 else ft.Colors.WHITE60
        self.btn_ingredientes.style.color = ft.Colors.WHITE if indice == 1 else ft.Colors.WHITE60

        # SE for para a aba de receitas, força a atualização do Dropdown
        if indice == 0:
            self.tela_receitas.content.carregar_dados()

        self.page.update()


def main(page: ft.Page):
    AppDoces(page)


if __name__ == "__main__":
    ft.app(target=main)