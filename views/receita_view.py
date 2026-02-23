import flet as ft

class ReceitaView(ft.Column):
    def __init__(self, db, app):
        super().__init__()
        self.db = db
        self.app = app
        self.id_receita_atual = None
        self.lista_itens_temporaria = []
        self.scroll = ft.ScrollMode.ADAPTIVE
        self.expand = True
        self.padding = ft.padding.only(top=10, left=10, right=10, bottom=40)

        # Campos
        self.txt_nome_receita = ft.TextField(label="Nome da Receita", dense=True, on_change=self.salvar_no_rascunho)
        self.txt_rendimento = ft.TextField(label="Rendimento", value="1", width=120, dense=True,
                                           keyboard_type=ft.KeyboardType.NUMBER, on_change=self.salvar_no_rascunho)
        self.txt_porcentagem = ft.TextField(label="Gastos Fixos (%)", value="0", suffix=ft.Text("%"), width=170,
                                            dense=True, keyboard_type=ft.KeyboardType.NUMBER,
                                            on_change=self.salvar_no_rascunho)

        self.sel_ingrediente = ft.Dropdown(label="Escolha um Ingrediente", expand=True)
        self.txt_quantidade = ft.TextField(label="Qtd", width=100, hint_text="Ex: 500")
        self.coluna_itens_visivel = ft.Column()

        self.btn_salvar = ft.ElevatedButton("Salvar Receita", bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE, icon=ft.Icons.SAVE, on_click=self.salvar_receita_completa, width=400)

        self.controls = [
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self.page.go_home()),
                    ft.Text("Voltar", size=16)]),
            ft.Text("Montar Receita", size=24, weight=ft.FontWeight.BOLD),
            self.txt_nome_receita,
            ft.Row([self.txt_rendimento, self.txt_porcentagem], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Divider(),
            ft.Row([self.sel_ingrediente, self.txt_quantidade]),
            ft.ElevatedButton("Adicionar Ingrediente", icon=ft.Icons.ADD, on_click=self.adicionar_item_lista),
            ft.Divider(),
            self.coluna_itens_visivel,
            ft.Divider(),
            self.btn_salvar
        ]
        self.on_mount = self.ao_montar

    def salvar_no_rascunho(self, e=None):
        self.app.rascunho = {
            "nome": self.txt_nome_receita.value,
            "rendimento": self.txt_rendimento.value,
            "porcentagem": self.txt_porcentagem.value,
            "itens": self.lista_itens_temporaria
        }

    def ao_montar(self, e):
        r = self.app.rascunho
        self.txt_nome_receita.value = r["nome"]
        self.txt_rendimento.value = r["rendimento"]
        self.txt_porcentagem.value = r["porcentagem"]
        self.lista_itens_temporaria = r["itens"]
        self.carregar_dados()
        self.atualizar_lista_visual()
        self.update()

    def carregar_dados(self):
        ing = self.db.ler_ingredientes()
        self.sel_ingrediente.options = [ft.DropdownOption(key=str(i[0]), text=f"{i[1]} ({i[2]})") for i in ing]

    def atualizar_lista_visual(self):
        self.coluna_itens_visivel.controls.clear()
        for item in self.lista_itens_temporaria:
            nome_ing = next((opt.text for opt in self.sel_ingrediente.options if opt.key == str(item['id'])),
                            "Ingrediente")
            self.coluna_itens_visivel.controls.append(
                ft.Container(bgcolor=ft.Colors.BLACK12, padding=10, border_radius=8, content=ft.Row([
                    ft.Text(f"{nome_ing} - {item['quantidade']}", expand=True),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color=ft.Colors.BLUE,
                        on_click=lambda e,
                        i=item: self.editar_item(i)),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        on_click=lambda e, i=item: self.remover_item(i))
                ]))
            )
        self.update()

    def editar_item(self, item):
        self.lista_itens_temporaria.remove(item)
        self.sel_ingrediente.value = str(item["id"])
        self.txt_quantidade.value = str(item["quantidade"])
        self.atualizar_lista_visual()

    def remover_item(self, item):
        self.lista_itens_temporaria.remove(item)
        self.salvar_no_rascunho()
        self.atualizar_lista_visual()

    def adicionar_item_lista(self, e):
        if self.sel_ingrediente.value and self.txt_quantidade.value:
            self.lista_itens_temporaria.append({"id": int(self.sel_ingrediente.value),
                                                "quantidade": float(self.txt_quantidade.value.replace(",", "."))})
            self.txt_quantidade.value = ""
            self.salvar_no_rascunho()
            self.atualizar_lista_visual()

    def limpar_campos(self):
        self.id_receita_atual = None
        self.app.rascunho = {"nome": "", "rendimento": "1", "porcentagem": "0", "itens": []}
        self.ao_montar(None)

    def preparar_edicao(self, dados):
        self.id_receita_atual = dados[0]
        self.txt_nome_receita.value = dados[1]
        self.txt_rendimento.value = str(dados[2])

        porcentagem_banco = dados[4] if len(dados) > 4 else 0
        self.txt_porcentagem.value = str(porcentagem_banco)

        self.btn_salvar.text = "Atualizar Receita"
        self.btn_salvar.color = ft.Colors.WHITE

        itens = self.db.buscar_itens_receita(self.id_receita_atual)
        self.lista_itens_temporaria = [{"id": i[3], "quantidade": i[1]} for i in itens]

        self.salvar_no_rascunho()
        self.atualizar_lista_visual()

    def salvar_receita_completa(self, e):
        try:
            n = self.txt_nome_receita.value
            r = float(self.txt_rendimento.value.replace(",", "."))
            p = float(self.txt_porcentagem.value.replace(",", "."))
            if self.id_receita_atual:
                self.db.atualizar_receita(self.id_receita_atual, n, r, p, self.lista_itens_temporaria)
            else:
                self.db.criar_receita(n, r, p, self.lista_itens_temporaria)
            self.limpar_campos()
            self.page.go_home()
        except Exception as err:
            print(f"Erro: {err}")