import flet as ft

class ReceitaView(ft.Column):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.id_receita_atual = None
        self.lista_itens_temporaria = []
        self.scroll = ft.ScrollMode.ADAPTIVE
        self.expand = True
        self.spacing = 20

        self.txt_nome_receita = ft.TextField(label="Nome da Receita", expand=True)
        self.txt_rendimento = ft.TextField(label="Rendimento", value="1", width=120)

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
            ft.Container(height=20),  # Um pequeno "respiro" no topo
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self.page.go_home()),
                ft.Text("Voltar para o Início", size=16)
            ]),

            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self.page.go_home()),
                ft.Text("Montar Receita", size=24, weight=ft.FontWeight.BOLD)
            ]),
            ft.Row([self.txt_nome_receita, self.txt_rendimento]),
            ft.Divider(),
            ft.Row([self.sel_ingrediente, self.txt_quantidade]),
            ft.ElevatedButton("Adicionar Ingrediente", icon=ft.Icons.ADD, on_click=self.adicionar_item_lista),
            ft.Divider(),
            ft.Text("Itens da Receita:", weight=ft.FontWeight.BOLD),
            self.coluna_itens_visivel,
            ft.Divider(),
            self.btn_salvar
        ]

    def carregar_dados(self):
        ingredientes = self.db.ler_ingredientes()
        self.sel_ingrediente.options = [
            ft.DropdownOption(key=str(i[0]), text=f"{i[1]} ({i[2]})") for i in ingredientes
        ]
        self.update()

    def limpar_campos(self):
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
        self.limpar_campos()

        self.id_receita_atual = dados[0]
        self.txt_nome_receita.value = dados[1]
        
        rend = dados[2]
        self.txt_rendimento.value = str(int(rend) if rend == int(rend) else rend)

        self.btn_salvar.text = "Atualizar Receita"
        self.btn_salvar.bgcolor = ft.Colors.ORANGE_800

        itens_do_banco = self.db.buscar_itens_receita(self.id_receita_atual)

        for item in itens_do_banco:
            item_dict = {"id": item[3], "quantidade": item[1]}
            self.lista_itens_temporaria.append(item_dict)

        self.atualizar_lista_visual()

    def atualizar_lista_visual(self):
        self.coluna_itens_visivel.controls.clear()
        
        if not self.lista_itens_temporaria:
            self.coluna_itens_visivel.controls.append(
                ft.Text("Nenhum ingrediente adicionado", italic=True, color="grey")
            )
        
        for item in self.lista_itens_temporaria:
            nome_ing = "Ingrediente"
            for opt in self.sel_ingrediente.options:
                if opt.key == str(item['id']):
                    nome_ing = opt.text
                    break
            
            qtd = item['quantidade']
            qtd_limpa = int(qtd) if qtd == int(qtd) else qtd

            btn_excluir = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=ft.Colors.RED_400,
                on_click=lambda e, i=item: self.remover_item(e, i)
            )

            linha = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=20),
                    ft.Text(f"{nome_ing} - {qtd_limpa}", expand=True),
                    btn_excluir, 
                ]),
                bgcolor=ft.Colors.BLACK12,
                padding=10,
                border_radius=8
            )
            
            self.coluna_itens_visivel.controls.append(linha)
        
        self.update()

    def adicionar_item_lista(self, e):
        if not self.sel_ingrediente.value or not self.txt_quantidade.value:
            return

        try:
            qtd = float(self.txt_quantidade.value.replace(",", "."))
            item_dict = {"id": int(self.sel_ingrediente.value), "quantidade": qtd}
            
            self.lista_itens_temporaria.append(item_dict)
            self.txt_quantidade.value = ""
            self.atualizar_lista_visual() 
            
        except ValueError:
            self.notificar("Digite um número válido!")

    def remover_item(self, e, item_dict):
        try:
            self.lista_itens_temporaria.remove(item_dict)
            self.atualizar_lista_visual()
        except Exception as err:
            print(f"Erro ao remover: {err}")

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