
import sqlite3
import sys
from datetime import datetime

from PySide6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QTableWidget, QAbstractItemView, \
    QPushButton, QLabel, QLineEdit, QWidget, QMessageBox


class EstoqueApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Controle de estoque')
        self.setGeometry(100, 100, 800, 400)

        # Criamops a conexão com db e cursor, ambos da instância
        self.conn = sqlite3.connect('estoque.db')
        self.cursor = self.conn.cursor()

        # Criamos a tabela
        self.criar_tabela()

        layout_principal = QHBoxLayout()
        layout_esquerda = QVBoxLayout()
        layout_direita = QVBoxLayout()
        layout_botoes = QHBoxLayout()

        # Tabela de produtos
        self.tbl_produtos = QTableWidget()
        # Removemos o header vertical da tabela
        self.tbl_produtos.verticalHeader().setVisible(False)
        # Marcamos que as células não serão editáveis
        self.tbl_produtos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Definimos que ao clicar em uma célula selecione toda a linha
        self.tbl_produtos.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Adicionamos a tabela ao layout da direita
        layout_direita.addWidget(self.tbl_produtos)


        # Criação de botões
        self.btn_cadastrar = QPushButton('Cadastrar')
        self.btn_remover = QPushButton('Remover')
        self.btn_editar = QPushButton('Editar')

        # Adicionamos os botões ao layout de botões (editar e remover)
        layout_botoes.addWidget(self.btn_editar)
        layout_botoes.addWidget(self.btn_remover)

        # Criação de campos e labels de input
        self.lbl_nome = QLabel('Nome do produto')
        self.txt_nome = QLineEdit()
        self.lbl_preco = QLabel('Preço do produto')
        self.txt_preco = QLineEdit()
        self.lbl_quantidade = QLabel('Quantidade em estoque')
        self.txt_quantidade = QLineEdit()
        self.lbl_data = QLabel('Data de validade')
        self.txt_data = QLineEdit()
        self.lbl_categoria = QLabel('Categoria')
        self.txt_categoria = QLineEdit()
        self.lbl_fornecedor = QLabel('Fornecedor')
        self.txt_fornecedor = QLineEdit()

        # Adicionamos os dados acima ao layout esquerdo
        layout_esquerda.addWidget(self.lbl_nome)
        layout_esquerda.addWidget(self.txt_nome)
        layout_esquerda.addWidget(self.lbl_preco)
        layout_esquerda.addWidget(self.txt_preco)
        layout_esquerda.addWidget(self.lbl_quantidade)
        layout_esquerda.addWidget(self.txt_quantidade)
        layout_esquerda.addWidget(self.lbl_data)
        layout_esquerda.addWidget(self.txt_data)
        layout_esquerda.addWidget(self.lbl_categoria)
        layout_esquerda.addWidget(self.txt_categoria)
        layout_esquerda.addWidget(self.lbl_fornecedor)
        layout_esquerda.addWidget(self.txt_fornecedor)
        layout_esquerda.addWidget(self.btn_cadastrar)
        layout_esquerda.addLayout(layout_botoes)

        # Adicionamos os layouts dir e esq ao principal
        layout_principal.addLayout(layout_esquerda)
        layout_principal.addLayout(layout_direita)

        # Adicionamos os layouts a janela principal
        central_widget = QWidget()
        central_widget.setLayout(layout_principal)
        self.setCentralWidget(central_widget)

        # Adicionamos as funções aos slotes através dos sinais
        self.btn_cadastrar.clicked.connect(self.inserir_produtos)

    def criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS produtos
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            preco REAL NOT NULL,
                            quantidade INTEGER NOT NULL,
                            data_validade TEXT,
                            categoria TEXT,
                            fornecedor TEXT)''')
        self.conn.commit()

    def inserir_produtos(self):
        if self.validar_data():
            try:
                self.cursor.execute("INSERT INTO produtos (nome, preco,"
                                    "quantidade, data_validade, categoria,"
                                    "fornecedor) "
                                    "VALUES (?, ?, ?, ?, ?, ?)", (self.txt_nome.text(),
                                                                  self.txt_preco.text(),
                                                                  self.txt_quantidade.text(),
                                                                  self.txt_data.text(),
                                                                  self.txt_categoria.text(),
                                                                  self.txt_fornecedor.text()))
                self.conn.commit()
                self.limpar_campos()
                QMessageBox.information(self,'Cadastro de produto',
                                        'Produto cadastrado com sucesso')
                self.limpar_campos()
            except Exception as e:
                print(e)

    def limpar_campos(self):
        self.txt_nome.clear()
        self.txt_preco.clear()
        self.txt_quantidade.clear()
        self.txt_data.clear()
        self.txt_categoria.clear()
        self.txt_fornecedor.clear()

    def validar_data(self):
        try:
            datetime.strptime(self.txt_data.text(), '%d/%m/%Y')
            return True
        except:
            QMessageBox.warning(self, 'Aviso', 'Data de validade fora do padrão '
                                               'dd/mm/aaaa')
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EstoqueApp()
    window.show()
    sys.exit(app.exec())
