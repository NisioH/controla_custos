import flet as ft

class ReceitaView(ft.Column):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.expand = True

        self.txt_nome_receita = ft.TextField(
            label="Nome da Receita",
            expand=True
        )

        self.txt_rendimento = ft.TextField(
            label="Rendimento (unidade/porções)",
            value="1"
        )

        self.sel_ingrediente = ft.Dropdown(
            label="Escolha um Ingrediente",
            expand=True,
            options=[]
        )

        self.txt_quantidade = ft.TextField(
            label="Qtd usada",
            width=120,
            hint_text="Ex: 395"
        )

        self.lista_itens_temporaria = []
        self.coluna_itens_visivel = ft.Column()

        self.btn_add_item = ft.ElevatedButton(
            "Adicionar à Receita",
            icon=ft.Icons.ADD_CIRCLE,
            on_click=self.adicionar_item_lista,
            width=400
        )

        self.btn_salver_receita = ft.ElevatedButton(
            "Finalizar e Salvar Receita",
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
            width=400,
            icon=ft.Icons.CHECK,
            on_click=self.salvar_receita_completa
        )

        self.controls = [
            ft.Text("Nova Receita", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([self.txt_nome_receita, self.txt_rendimento]),
            ft.Divider(),
            ft.Text("Ingredientes da Receita", size=18, weight=ft.FontWeight.W_500),
            ft.Row([self.sel_ingrediente, self.txt_quantidade]),
            self.btn_add_item,
            ft.Divider(),
            ft.Text("Itens Adicionados", weight=ft.FontWeight.BOLD),
            self.coluna_itens_visivel,
            ft.Divider(),
            self.btn_salver_receita
        ]

        self.on_mount = self.ao_montar

    def ao_montar(self, e):
        self.carregar_dados()

    def carregar_dados(self):
        ingredientes = self.db.ler_ingredientes()

        self.sel_ingrediente.options = []

        if ingredientes:
            for ing in ingredientes:
                self.sel_ingrediente.options.append(
                    ft.DropdownOption(key=str(ing[0]), text=f"{ing[1]} ({ing[2]})")
                )
        else:
            self.sel_ingrediente.options.append(
                ft.DropdownOption(text="Nenhum ingrediente encontrado")
            )

        self.update()

    def adicionar_item_lista(self, e):
        if not self.sel_ingrediente.value or not self.txt_quantidade.value:
            self.notificar("Selecione um ingrediente e a quantidade!")
            return

        nome_ing = ""
        for opt in self.sel_ingrediente.options:
            if opt.key == self.sel_ingrediente.value:
                nome_ing = opt.text
                break

        self.lista_itens_temporaria.append({
            "id": int(self.sel_ingrediente.value),
            "quantidade": float(self.txt_quantidade.value.replace(",", "."))
        })

        self.coluna_itens_visivel.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN),
                    ft.Text(f"{nome_ing} - Qtd: {self.txt_quantidade.value}", size=16, expand=True),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400,
                                  on_click=lambda _: self.remover_item_da_temp(nome_ing))
                ]),
                bgcolor=ft.Colors.GREY_100,
                padding=10,
                border_radius=10,
            )
        )
        self.txt_quantidade.value = ""
        self.update()

    def remover_item_da_temp(self, nome):
        self.notificar(f"Removido {nome} da lista!")

    def salvar_receita_completa(self, e):
        nome = self.txt_nome_receita.value
        rendimento = self.txt_rendimento.value

        if not nome or not self.lista_itens_temporaria:
            self.notificar("Preencha o nome e adicione ingredientes!")
            return

        try:
            self.db.criar_receita(nome, float(rendimento), self.lista_itens_temporaria)
            self.txt_nome_receita.value = ""
            self.lista_itens_temporaria = []
            self.coluna_itens_visivel.controls.clear()
            self.notificar(f"Receita {nome} salva com sucesso!")
            self.update()

        except Exception as err:
            self.notificar(f"Erro ao salvar receita: {err}")

    def notificar(self, msg):
        if self.page:
            self.page.snack_bar = ft.SnackBar(ft.Text(msg))
            self.page.snack_bar.open = True
            self.page.update()