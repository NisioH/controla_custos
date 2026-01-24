import flet as ft

class DashboardView(ft.Column):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.expand = True
        self.scroll = ft.ScrollMode.ADAPTIVE

        self.lista_receitas = ft.Column(spacing=10)

        self.controls = [
            ft.Text("Minhas Receitas", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Resumo de custos e lucros", color=ft.Colors.WHITE_600),
            ft.Divider(),
            self.lista_receitas,
        ]

    def carregar_dados(self):
        self.lista_receitas.controls.clear()
        receitas = self.db.ler_receitas()

        if not receitas:
            self.lista_receitas.controls.append(
                ft.Container(
                    content=ft.Text("Nenhuma receita salva.", size=16),
                    padding=20,
                    alignment=ft.alignment.center
                )
            )
        else:
            for rec in receitas:
                id_rec, nome, rendimento, custo_total = rec
                custo_unitario = custo_total / rendimento if rendimento > 0 else 0

                self.lista_receitas.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.COOKIE, color=ft.Colors.AMBER),
                                title=ft.Text(f"Rendimento: {rendimento} porções"),
                                trailing=ft.Text(f"Custo Total: \nR$ {custo_total: .2f}",
                                                 text_align=ft.TextAlign.RIGHT,
                                                 color=ft.Colors.GREEN_400),
                            ),
                            ft.Padding(
                                padding=ft.EdgeInsets.only(left=70, bottom=10),
                                content=ft.Text(f"Custo por unidade: R$ {custo_unitario: .2f}",
                                                size=12,
                                                italic=True)
                            )
                        ]),
                        bgcolor=ft.Colors.BLUE_GREY_800,
                        border_radius=10,
                        on_click=lambda _, r=rec: print(f"Clicou na receita: {r[1]}")
                    )
                )
        self.update()