# 🧁 App Gestão de Doces

Aplicativo desenvolvido em **Python** com **Flet** para controle de custos e precificação de Geladinhos e Bolos. Projeto focado em usabilidade mobile e organização modular por classes.

## 📐 Estrutura do Projeto

O projeto é dividido em módulos para facilitar a manutenção:
- `main.py`: Ponto de entrada e gerenciamento de navegação (Abas).
- `database.py`: Classe `Database` que isola toda a lógica do SQLite.
- `views/`: Pasta contendo as interfaces divididas por componentes.

## 🛠️ Tecnologias
- Python 3.x
- Flet (UI Framework)
- SQLite (Banco de Dados)

## 📋 Funcionalidades
- [ ] Cadastro de Ingredientes com preço e unidade.
- [ ] Criação de Receitas com seleção de itens existentes.
- [ ] Cálculo automático de custo por porção.
- [ ] Interface adaptativa para teclados mobile.

## 🚀 Como Rodar
1. Instale as dependências: `pip install -r requirements.txt`
2. Execute o projeto: `python main.py`

## 📱 Testar no Celular
Existem duas formas principais de testar o aplicativo diretamente no seu celular:

### Opção 1: Usando o App do Flet (Recomendado)
Esta opção permite ver o app com comportamento nativo:
1. Instale o aplicativo **Flet** na Google Play Store ou Apple App Store.
2. Certifique-se de que seu celular e computador estão na **mesma rede Wi-Fi**.
3. No terminal do seu computador, execute:
   ```bash
   flet run --android
   ```
   (ou `flet run --ios` se estiver no Mac).
4. Um QR Code aparecerá no terminal. Abra o app Flet no celular e escaneie o código.

### Opção 2: Pelo Navegador do Celular
1. No arquivo `main.py`, altere a linha final para:
   ```python
   ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)
   ```
2. Descubra o endereço IP do seu computador na rede local (ex: `192.168.1.10`).
3. No navegador do seu celular, acesse: `http://<seu-ip>:8550`

## 📦 Inicializar Git
Para versionar o projeto: