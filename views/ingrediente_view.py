import flet as ft

class IngredienteView(ft.Column):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.expand = True
        self.id_ingrediente_atual = None

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
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    border_radius=10
                )
            )
        self.update()

    def salvar_clicado(self, e):
        nome = self.txt_nome.value
        unidade = self.txt_unidade.value
        str_preco = self.txt_preco_compra.value
        str_peso = self.txt_peso_embalagem.value

        # 1. Validação de campos vazios
        if not nome or not str_preco or not str_peso:
            self.notificar("Por favor, preencha todos os campos antes de salvar.")
            return

        try:
            # 2. Conversão segura (aqui o erro ValueError pode acontecer se tiver letras)
            preco = float(str_preco.replace(",", "."))
            peso = float(str_peso.replace(",", "."))

            if self.id_ingrediente_atual:
                self.db.atualizar_ingrediente(self.id_ingrediente_atual, nome, unidade, preco, peso)
                self.notificar("Ingrediente atualizado com sucesso!")
            else:
                self.db.criar_ingrediente(nome, unidade, preco, peso)
                self.notificar("Ingrediente criado com sucesso!")

            self.limpar_campos()
            self.carregar_dados()

        except ValueError:
            # 3. Avisa o usuário caso ele tenha digitado texto no lugar de números
            self.notificar("Erro: Digite apenas valores numéricos válidos para preço e peso.")
        except Exception as err:
            self.notificar(f"Erro ao salvar: {err}")

    def preparar_edicao(self, dados):
        self.id_ingrediente_atual = dados[0] 
        self.txt_nome.value = dados[1]
        self.txt_unidade.value = dados[2]
        self.txt_preco_compra.value = str(dados[3])
        self.txt_peso_embalagem.value = str(dados[4])
        
        self.btn_salvar.text = "Atualizar Ingrediente"
        self.btn_salvar.color = ft.Colors.WHITE
        self.update()

    def deletar(self, id_ing):
        self.db.deletar_ingrediente(id_ing)
        self.carregar_dados()
        self.notificar("Removido!")

    def limpar_campos(self):
        self.id_ingrediente_atual = None
        self.txt_nome.value = ""
        self.txt_unidade.value = "g"
        self.txt_preco_compra.value = ""
        self.txt_peso_embalagem.value = ""
        self.btn_salvar.text = "Salvar no Estoque"
        self.btn_salvar.color = ft.Colors.BLUE_700
        self.update()

    def notificar(self, msg):
        if self.page:
            self.page.snack_bar = ft.SnackBar(ft.Text(msg))
            self.page.snack_bar.open = True
            self.page.update()