import flet as ft

class IngredienteView(ft.Column):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.expand = True
        self.id_em_edicao = None

        # --- Campos de Entrada ---
        self.txt_nome = ft.TextField(label="Nome do Ingrediente:", expand=True)
        self.txt_unidade = ft.Dropdown(
            label="Und", width=110,
            options=[
                ft.DropdownOption("g"),
                ft.DropdownOption("ml"),
                ft.DropdownOption("un")
            ]
        )
        self.txt_preco_compra = ft.TextField(label="Preço Pago (R$)", expand=1)
        self.txt_peso_embalagem = ft.TextField(label="Peso/Qtd na Embalagem", expand=1, hint_text="Ex: 395")

        self.btn_salvar = ft.ElevatedButton(
            "Salvar no Estoque",
            icon=ft.Icons.SAVE,
            on_click=self.salvar_clicado,
            width=400,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE
        )

        self.lista_ingredientes = ft.ListView(expand=True, spacing=10)

        # --- Layout da Tela ---
        self.controls = [
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: self.page.go_home()
                ),
                ft.Text("Voltar para o Início")
            ]),

            ft.Text("Cadastro de Ingredientes", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([self.txt_nome, self.txt_unidade]),
            ft.Row([self.txt_preco_compra, self.txt_peso_embalagem]),
            self.btn_salvar,
            ft.Divider(),
            self.lista_ingredientes
        ]

        self.on_mount = self.ao_montar

    def ao_montar(self, e):
        self.carregar_dados()

    def carregar_dados(self):
        self.lista_ingredientes.controls.clear()
        dados = self.db.ler_ingredientes()

        for ing in dados:
            self.lista_ingredientes.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        title=ft.Text(ing[1], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"R$ {ing[3]:.2f} por {ing[4]}{ing[2]}"),
                        trailing=ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color=ft.Colors.BLUE,
                                on_click=lambda e, i=ing: self.preparar_edicao(i)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                on_click=lambda e, id_i=ing[0]: self.deletar(id_i)
                            )
                        ], tight=True),
                    ),
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=10
                )
            )
        self.update()

    def salvar_clicado(self, e):
        # 1. Captura os valores
        nome = self.txt_nome.value
        unidade = self.txt_unidade.value  # Ex: kg, g, ml
        preco = self.txt_preco_compra.value
        peso = self.txt_peso_embalagem.value

        # 2. Validação simples
        if not nome or not preco or not peso:
            self.notificar("Preencha todos os campos!")
            return

        try:
            # 3. Converte para os formatos corretos (importante!)
            preco_float = float(preco.replace(",", "."))
            peso_float = float(peso.replace(",", "."))

            # 4. Envia para o banco
            self.db.criar_ingrediente(nome, unidade, preco_float, peso_float)

            # 5. Limpa os campos e avisa o usuário
            self.txt_nome.value = ""
            self.txt_preco_compra.value = ""
            self.txt_peso_embalagem.value = ""
            self.carregar_dados()  # Atualiza a listinha na tela
            self.notificar(f"Ingrediente {nome} salvo!")

        except ValueError:
            self.notificar("Preço e Peso devem ser números!")

    def preparar_edicao(self, ingrediente):
        self.id_em_edicao = ingrediente[0]
        self.txt_nome.value = ingrediente[1]
        self.txt_unidade.value = ingrediente[2]
        self.txt_preco_compra.value = str(ingrediente[3])
        self.txt_peso_embalagem.value = str(ingrediente[4])
        self.btn_salvar.text = "Atualizar Cadastro"
        self.btn_salvar.color = ft.Colors.ORANGE_700
        self.txt_nome.focus()
        self.update()

    def deletar(self, id_ing):
        self.db.deletar_ingrediente(id_ing)
        self.carregar_dados()
        self.notificar("Removido!")

    def limpar_campos(self):
        self.txt_nome.value = ""
        self.txt_preco_compra.value = ""
        self.txt_peso_embalagem.value = ""
        self.id_em_edicao = None
        self.btn_salvar.text = "Salvar no Estoque"
        self.btn_salvar.color = ft.Colors.BLUE_700
        self.update()

    def notificar(self, msg):
        if self.page:
            self.page.snack_bar = ft.SnackBar(ft.Text(msg))
            self.page.snack_bar.open = True
            self.page.update()