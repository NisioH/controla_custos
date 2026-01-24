import sqlite3
from contextlib import contextmanager


class Database:
    def __init__(self):
        self.db_name = "gestao_doces.db"
        self.init_db()

    @contextmanager
    def abrir_cursor(self):
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_db(self):
        with self.abrir_cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ingredientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    unidade TEXT NOT NULL,
                    preco REAL NOT NULL,
                    peso_embalagem REAL NOT NULL DEFAULT 1
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS receitas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    rendimento REAL NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS receitas_itens (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                           id_receita INTEGER,
                                                              id_ingrediente INTEGER,
                                                              qtd_usada REAL,
                                                              FOREIGN KEY(id_receita) REFERENCES receitas (id),
                    FOREIGN KEY (id_ingrediente) REFERENCES ingredientes (id)
                )
            """)

    def criar_ingrediente(self, nome, unidade, preco, peso_embalagem):
        with self.abrir_cursor() as cursor:
            cursor.execute("INSERT INTO ingredientes (nome, unidade, preco, peso_embalagem) VALUES (?, ?, ?, ?)",
                           (nome, unidade, preco, peso_embalagem))

    def ler_ingredientes(self):
        with self.abrir_cursor() as cursor:
            cursor.execute("SELECT id, nome, unidade, preco, peso_embalagem FROM ingredientes ORDER BY nome")
            return cursor.fetchall()

    def atualizar_ingrediente(self, id_ing, nome, unidade, preco, peso_embalagem):
        with self.abrir_cursor() as cursor:
            cursor.execute("UPDATE ingredientes SET nome=?, unidade=?, preco=?, peso_embalagem=? WHERE id=?",
                           (nome, unidade, preco, peso_embalagem, id_ing))

    def deletar_ingrediente(self, id_ing):
        with self.abrir_cursor() as cursor:
            cursor.execute("DELETE FROM ingredientes WHERE id=?", (id_ing,))

    def criar_receita(self, nome, rendimento, itens):
        with self.abrir_cursor() as cursor:
            cursor.execute("INSERT INTO receitas (nome, rendimento) VALUES (?, ?)",
                           (nome, rendimento))
            id_receita = cursor.lastrowid
            for item in itens:
                cursor.execute("INSERT INTO receitas_itens (id_receita, id_ingrediente, qtd_usada) "
                               "VALUES (?, ?, ?)", (id_receita, item['id'], item['quantidade']))

    def ler_receita(self):
        query = '''
                SELECT r.id, \
                       r.nome, \
                       r.rendimento,
                       COALESCE(SUM((i.preco / i.peso_embalagem) * ri.qtd_usada), 0) AS custo_total
                FROM receitas r
                         LEFT JOIN receitas_itens ri ON r.id = ri.id_receita
                         LEFT JOIN ingredientes i ON ri.id_ingrediente = i.id
                GROUP BY r.id
                ORDER BY r.nome \
                '''
        with self.abrir_cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def atualizar_receita(self, id_rec, nome, rendimento, novos_itens):
        with self.abrir_cursor() as cursor:
            cursor.execute("UPDATE receitas SET nome=?, rendimento=? WHERE id=?",
                           (nome, rendimento, id_rec))
            cursor.execute("DELETE FROM receitas_itens WHERE id_receita=?",
                           (id_rec,))
            for item in novos_itens:
                cursor.execute("INSERT INTO receitas_itens "
                               "(id_receita, id_ingrediente, qtd_usada) VALUES (?, ?, ?)",
                               (id_rec, item['id'], item['quantidade']))

    def deletar_receita(self, id_rec):
        with self.abrir_cursor() as cursor:
            cursor.execute("DELETE FROM receitas_itens WHERE id_receita=?", (id_rec,))
            cursor.execute("DELETE FROM receitas WHERE id=?", (id_rec,))

    def buscar_itens_receita(self, id_rec):
        query = '''
            SELECT i.nome, ri.qtd_usada, i.unidade
            FROM receitas_itens ri
            JOIN ingredientes i ON ri.id_ingrediente = i.id
            WHERE ri.id_receita = ?
        '''
        with self.abrir_cursor() as cursor:
            cursor.execute(query, (id_rec,))
            return cursor.fetchall()
        