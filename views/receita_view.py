import flet as ft

class ReceitaView(ft.Column):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.id_receita_atual = None
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
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: self.page.go_home()
                ),
                ft.Text("Voltar para o Início")
            ]),
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

    def preparar_edicao(self, dados_receita):
        self.id_receita_atual = dados_receita[0]
        self.txt_nome_receita.value = dados_receita[1]
        self.txt_rendimento.value = str(dados_receita[2])

        self.btn_salver_receita.text = "Atualizar Receita"
        self.btn_salver_receita.bgcolor = ft.Colors.ORANGE_800

        self.carregar_itens_da_receita(self.id_receita_atual)
        self.update()

    def carregar_itens_da_receita(self, id_rec):
        self.lista_itens_temporaria = []
        self.coluna_itens_visivel.controls.clear()
        itens = self.db.buscar_itens_receita(id_rec)

        for item in itens:
            qtd = item[1]
            qtd_limpa = int(qtd) if qtd == int(qtd) else qtd
            self.coluna_itens_visivel.controls.append(
                ft.Text(f". {item[0]}: {qtd_limpa}{item[2]}")
            )

    def adicionar_item_lista(self, e):
        # 1. Validação: Verifica se algo foi selecionado e se a quantidade foi digitada
        if not self.sel_ingrediente.value or not self.txt_quantidade.value:
            self.notificar("Selecione um ingrediente e a quantidade!")
            return

        try:
            # 2. Tratamento do número: converte vírgula para ponto e remove o .0 se for inteiro
            valor_digitado = float(self.txt_quantidade.value.replace(",", "."))
            qtd_limpa = int(valor_digitado) if valor_digitado == int(valor_digitado) else valor_digitado

            # 3. Busca o nome e a unidade do ingrediente selecionado para exibir na lista
            nome_exibicao = ""
            for opt in self.sel_ingrediente.options:
                if opt.key == self.sel_ingrediente.value:
                    nome_exibicao = opt.text # Ex: "Açúcar (kg)"
                    break

            # 4. Adiciona à lista "invisível" (que vai para o banco de dados)
            item_temp = {
                "id": int(self.sel_ingrediente.value),
                "quantidade": valor_digitado
            }
            self.lista_itens_temporaria.append(item_temp)

            # 5. Adiciona à lista "visível" (o que as suas filhas veem na tela)
            self.coluna_itens_visivel.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_400, size=20),
                        ft.Text(f"{nome_exibicao} - Qtd: {qtd_limpa}", size=16, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color=ft.Colors.RED_400,
                            tooltip="Remover este item",
                            on_click=lambda _: self.remover_item_da_temp(item_temp, nome_exibicao)
                        )
                    ]),
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    padding=10,
                    border_radius=8,
                    margin=ft.margin.only(bottom=5)
                )
            )

            # 6. Limpa o campo de quantidade e foca no dropdown para o próximo ingrediente
            self.txt_quantidade.value = ""
            self.txt_quantidade.focus()
            self.update()

        except ValueError:
            self.notificar("Por favor, digite um número válido na quantidade!")

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

    def remover_item_da_temp(self, item_dict, nome_para_aviso):
        try:
            self.lista_itens_temporaria.remove(item_dict)

            self.coluna_itens_visivel.controls.clear()

            for item in self.lista_itens_temporaria:
                nome_ing = "Ingreiente"
                for opt in self.sel_ingrediente.options:
                    if opt.key == str(item["id"]):
                        nome_ing = opt.text
                        break

                qtd_limpa = int(item["quantidade"]) if item["quantidade"] == int(item["quantidade"]) else item["quantidade"]
                self.coluna_itens_visivel.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_400, size=20),
                            ft.Text(f"{nome_ing} - Qtd: {qtd_limpa}", size=16, expand=True),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED_400,
                                tooltip="Remover este item",
                                on_click=lambda _: self.remover_item_da_temp(item, nome_para_aviso)
                            )
                        ]),
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        padding=10,
                        border_radius=8,
                        margin=ft.margin.only(bottom=5)
                    )
                )
            self.notificar(f"Removido {nome_para_aviso} da lista!")
            self.update()
        except Exception as err:
            self.notificar(f"Erro ao remover item da lista: {err}")

    def notificar(self, msg):
        if self.page:
            self.page.snack_bar = ft.SnackBar(ft.Text(msg))
            self.page.snack_bar.open = True
            self.page.update()