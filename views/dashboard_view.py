import flet as ft


class DashboardView(ft.Column):
    def __init__(self, db, ao_editar):
        super().__init__()
        self.db = db
        self.ao_editar = ao_editar  # Função que vem do main.py para abrir a edição
        self.expand = True

        # Lista onde as receitas serão desenhadas
        self.lista_receitas = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE)

        self.controls = [
            ft.Text("Minhas Receitas", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Resumo de custos e lucros", color=ft.Colors.WHITE60),
            ft.Divider(),
            self.lista_receitas
        ]

    def carregar_dados(self):
        """Busca as receitas no banco e monta os cards na tela"""
        self.lista_receitas.controls.clear()
        receitas = self.db.ler_receita()

        if not receitas:
            self.lista_receitas.controls.append(
                ft.Text("Nenhuma receita cadastrada ainda.",
                        italic=True, color=ft.Colors.GREY_400)
            )
        else:
            for rec in receitas:
                # rec = (id, nome, rendimento, custo_total)
                id_rec, nome, rendimento, custo_total = rec

                rendimento_val = rendimento if rendimento > 0 else 1

                custo_unitario = custo_total / rendimento_val

                # Limpando o .0 do rendimento (ex: 2.0 vira 2)
                rend_limpo = int(rendimento) if rendimento == int(rendimento) else rendimento

                self.lista_receitas.controls.append(
                    ft.Container(
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        border_radius=12,
                        padding=5,
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.COOKIE, color=ft.Colors.AMBER, size=30),
                            title=ft.Text(nome, weight=ft.FontWeight.BOLD, size=18),
                            subtitle=ft.Text(f"Rendimento: {rend_limpo} porções | "
                                             f"Custo Unitário: R$ {custo_unitario:.2f}"),
                            # Lado direito: Preço e Botão Excluir
                            trailing=ft.Row([
                                ft.Text(f"R$ {custo_total:.2f}",
                                        color=ft.Colors.GREEN_400,
                                        weight=ft.FontWeight.BOLD,
                                        size=16),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Excluir Receita",
                                    on_click=lambda e, r_id=id_rec: self.deletar_e_atualizar(e, r_id)
                                ),
                            ], tight=True),
                            # Clique no card para editar
                            on_click=lambda _, r=rec: self.ao_editar(r)
                        ),

                    )
                )
        self.update()

    def deletar_e_atualizar(self, e, r_id):
        """Chama o banco para excluir e atualiza a lista na hora"""
        self.db.deletar_receita(r_id)
        self.carregar_dados()  # Recarrega a lista para a receita sumir

        # Mostra um aviso rápido embaixo
        self.page.snack_bar = ft.SnackBar(
            ft.Text("Receita excluída com sucesso!"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()