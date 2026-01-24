import flet as ft

class ReceitaView(ft.Column):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.id_receita_atual = None
        self.lista_itens_temporaria = []
        self.expand = True

        self.txt_nome_receita = ft.TextField(label="Nome da Receita", expand=True)
        self.txt_rendimento = ft.TextField(label="Rendimento", value="1", width=100)

        self.sel_ingrediente = ft.Dropdown(label="Escolha um Ingrediente", expand=True)
        self.txt_quantidade = ft.TextField(label="Qtd", width=100, hint_text="Ex: 500")

        self.coluna_itens_visivel = ft.Column()

        self.btn_salvar = ft.ElevatedButton(
            "Finalizar e Salvar Receita",
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
            icon=ft.Icons.SAVE,
            on_click=self.salvar_receita_completa,
            width=400
        )

        self.controls = [
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self.page.go_home()),
                ft.Text("Montar Receita", size=24, weight="bold")
            ]),
            ft.Row([self.txt_nome_receita, self.txt_rendimento]),
            ft.Divider(),
            ft.Row([self.sel_ingrediente, self.txt_quantidade]),
            ft.ElevatedButton("Adicionar Ingrediente", icon=ft.Icons.ADD, on_click=self.adicionar_item_lista),
            ft.Divider(),
            ft.Text("Itens da Receita:", weight="bold"),
            self.coluna_itens_visivel,
            ft.Divider(),
            self.btn_salvar
        ]

    def carregar_dados(self):
        """Preenche o dropdown de ingredientes"""
        ingredientes = self.db.ler_ingredientes()
        self.sel_ingrediente.options = [
            ft.DropdownOption(key=str(i[0]), text=f"{i[1]} ({i[2]})") for i in ingredientes
        ]
        self.update()

    def limpar_campos(self):
        """Limpa a tela para uma NOVA receita"""
        self.id_receita_atual = None
        self.txt_nome_receita.value = ""
        self.txt_rendimento.value = "1"
        self.txt_quantidade.value = ""
        self.lista_itens_temporaria = []
        self.coluna_itens_visivel.controls.clear()
        self.btn_salvar.text = "Finalizar e Salvar Receita"
        self.btn_salvar.bgcolor = ft.Colors.GREEN_700
        self.update()

    def preparar_edicao(self, dados):
        """Preenche a tela com os dados de uma receita existente"""
        self.limpar_campos()
        self.id_receita_atual = dados[0]
        self.txt_nome_receita.value = dados[1]
        self.txt_rendimento.value = str(int(dados[2]) if dados[2] == int(dados[2]) else dados[2])

        self.btn_salvar.text = "Atualizar Receita"
        self.btn_salvar.bgcolor = ft.Colors.ORANGE_800

        itens = self.db.buscar_itens_receita(self.id_receita_atual)

        for item in itens:
            self.coluna_itens_visivel.controls.append(ft.Text(f"• {item[0]}: {item[1]} {item[2]}"))
        self.update()

    def adicionar_item_lista(self, e):
        if not self.sel_ingrediente.value or not self.txt_quantidade.value:
            return

        valor = float(self.txt_quantidade.value.replace(",", "."))
        qtd_limpa = int(valor) if valor == int(valor) else valor

        nome_ing = ""
        for opt in self.sel_ingrediente.options:
            if opt.key == self.sel_ingrediente.value:
                nome_ing = opt.text
                break

        item_dict = {"id": int(self.sel_ingrediente.value), "quantidade": valor}
        self.lista_itens_temporaria.append(item_dict)

        self.coluna_itens_visivel.controls.append(
            ft.Row([
                ft.Icon(ft.Icons.CHECK, color="green"),
                ft.Text(f"{nome_ing} - {qtd_limpa}", expand=True),
                ft.IconButton(ft.Icons.DELETE, on_click=lambda _: self.remover_item(item_dict))
            ])
        )
        self.txt_quantidade.value = ""
        self.update()

    def remover_item(self, item_dict):
        self.lista_itens_temporaria.remove(item_dict)
        self.notificar("Item removido. Adicione os outros.")
        self.update()

    def salvar_receita_completa(self, e):
        nome = self.txt_nome_receita.value
        try:
            rend = float(self.txt_rendimento.value.replace(",", "."))
            if self.id_receita_atual:
                self.db.atualizar_receita(self.id_receita_atual, nome, rend, self.lista_itens_temporaria)
            else:
                self.db.criar_receita(nome, rend, self.lista_itens_temporaria)

            self.limpar_campos()
            self.page.go_home()
            self.notificar("Sucesso!")
        except Exception as err:
            self.notificar(f"Erro: {err}")

    def notificar(self, msg):
        self.page.snack_bar = ft.SnackBar(ft.Text(msg))
        self.page.snack_bar.open = True
        self.page.update()