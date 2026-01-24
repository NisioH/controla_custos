import flet as ft


class DashboardView(ft.Column):
    def __init__(self, db, ao_editar):
        super().__init__()
        self.db = db
        self.ao_editar = ao_editar
        self.expand = True
        self.lista_receitas = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE)

        self.controls = [
            ft.Text("Minhas Receitas", size=28, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            self.lista_receitas
        ]

    def carregar_dados(self):
        self.lista_receitas.controls.clear()
        receitas = self.db.ler_receita()

        for rec in receitas:
            id_rec, nome, rendimento, custo_total = rec


            rendimento_limpo = int(rendimento) if rendimento == int(rendimento) else rendimento

            self.lista_receitas.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.COOKIE, color=ft.Colors.AMBER),
                        title=ft.Text(nome, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Rendimento: {rendimento_limpo} un"),
                        trailing=ft.Text(f"R$ {custo_total:.2f}",
                                         color=ft.Colors.GREEN_400,
                                         weight=ft.FontWeight.BOLD,
                                         size=16),
                    ),
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    border_radius=10,
                    on_click=lambda _, r=rec: self.ao_editar(r)
                )
            )
        self.update()