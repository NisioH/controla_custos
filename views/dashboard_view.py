from flet.controls.core.canvas import color

import flet as ft


class DashboardView(ft.Column):
    def __init__(self, db, ao_editar):
        super().__init__()
        # ... (seu código de inicialização permanece o mesmo) ...
        self.db = db
        self.ao_editar = ao_editar
        self.expand = True
        self.scroll = ft.ScrollMode.ADAPTIVE
        self.padding = ft.padding.only(top=10, left=15, right=15, bottom=20)
        self.spacing = 20

        self.lista_receitas = ft.Column(spacing=10)

        self.controls = [
            ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CAKE_ROUNDED, color=ft.Colors.PINK_500, size=50),
                    ft.Text("Minhas Receitas!!!", size=28, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(height=10),
                self.lista_receitas,
                ft.Container(height=50)
            ])
        ]

    def carregar_dados(self):
        self.lista_receitas.controls.clear()
        receitas = self.db.ler_receita()

        if not receitas:
            self.lista_receitas.controls.append(
                ft.Text("Nenhuma receita cadastrada ainda.",
                        italic=True, color=ft.Colors.GREY_400)
            )
        else:
            for rec in receitas:
                id_rec, nome, rendimento, custo_total, porcentagem = rec

                custo_seguro = custo_total if custo_total is not None else 0.0
                rendimento_val = rendimento if rendimento > 0 else 1
                custo_unitario = custo_seguro / rendimento_val

                # CÁLCULO MANTIDO: Sugestão de Preço de Venda Unitário (+100%)
                venda_sugerida_unidade = custo_unitario * 2

                rend_limpo = int(rendimento) if rendimento == int(rendimento) else rendimento

                # --- NOVO DESIGN RESPONSIVO (PERFEITO PARA CELULAR) ---
                self.lista_receitas.controls.append(
                    ft.Container(
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        border_radius=15,
                        padding=15,  # Padding ajustado

                        # Usando Row em vez de ListTile para controle total do espaço
                        content=ft.Row([

                            # 1. Ícone
                            ft.Icon(ft.Icons.COOKIE, color=ft.Colors.AMBER, size=35),

                            # 2. Textos (O expand=True aqui é a mágica que evita espremer o texto)
                            ft.Column([
                                ft.Text(nome, weight=ft.FontWeight.BOLD, size=18),
                                ft.Text(
                                    f"Rend.: {rend_limpo} un | +{porcentagem}%\n"
                                    f"Custo: R$ {custo_unitario:.2f}",
                                    size=13,
                                    color=ft.Colors.WHITE70
                                ),
                            ], expand=True, spacing=2),

                            # 3. Crachá de Venda (Sem width fixo, se ajusta ao conteúdo)
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Venda Sugerida", size=11, color=ft.Colors.GREEN_100),
                                    ft.Text(f"R$ {venda_sugerida_unidade:.2f}",
                                            size=18,  # Fonte um pouquinho menor para caber melhor no mobile
                                            color=ft.Colors.GREEN_ACCENT_400,
                                            weight=ft.FontWeight.BOLD),
                                ], alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, tight=True),
                                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
                                border_radius=10,
                                padding=ft.padding.symmetric(horizontal=8, vertical=5),
                            ),

                            # 4. Botão de Exclusão
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED_400,
                                tooltip="Excluir Receita",
                                on_click=lambda e, r_id=id_rec: self.deletar_e_atualizar(e, r_id)
                            )

                        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),

                        # O clique no container inteiro edita a receita (igual era no ListTile)
                        on_click=lambda _, r=rec: self.ao_editar(r)
                    )
                )
        self.update()

    # ... (restante do código permanece o mesmo) ...

    def deletar_e_atualizar(self, e, r_id):
        self.db.deletar_receita(r_id)
        self.carregar_dados()

        self.page.snack_bar = ft.SnackBar(
            ft.Text("Receita excluída com sucesso!"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()