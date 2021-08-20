# Importar a classe da GUI feita no PyQT5

# Instanciar a nossa classe

import sys
from conexoes import Add_Historico, Carregar_Produto, Verificar_Codigo, Att_Estoque
from adm import Acessar_Adm
from design2 import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem

titulos = ['Código', 'Nome', 'Quantidade', 'Preço Unitário', 'Preço Total']

novoProduto = {
    'Codigo': 11111,
    'Nome': 'Bolacha',
    'Quant': 5,
    'PrecoUnit': 10,
    'PrecoTot': 50
}


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):  # Construtor do APP
        super().__init__()  # Chama o construtor padrão da biblioteca PyQT5
        super().setupUi(self)  # Chama o construtor setupUi do design.py

        # Adiciona o nome de cada coluna à tabela do carrinho, na ordem do array titulos
        self.tabCarrinho.setColumnCount(len(titulos))
        self.tabCarrinho.setHorizontalHeaderLabels(titulos)

        # Adicionar as conexões intrínsecas a cada botão
        self.btnAdicionar.clicked.connect(self.Add_Carrinho)
        self.btnRemover.clicked.connect(self.Concluir_Compra)
        self.btnLimpar.clicked.connect(self.Limpar_Carrinho)

    def Add_Carrinho(self):
        codigo = self.txtCod.text()

        if Verificar_Codigo(self, codigo):
            # Traz o produto do banco de dados
            produto = Carregar_Produto(codigo)

            # Descobre a quantidade de linhas na tabela
            linhasCount = self.tabCarrinho.rowCount()

            # Adiciona uma nova linha, por meio do index dela
            self.tabCarrinho.insertRow(linhasCount)

            # Cria as variáveis dos itens para adicionar na nova linha
            codigo = QTableWidgetItem(str(produto['Codigo']))
            nome = QTableWidgetItem(produto['Nome'])
            quant = QTableWidgetItem(str(produto['Quant']))
            precoUnit = QTableWidgetItem(str(produto['PrecoUnit']))
            precoTot = QTableWidgetItem(str(produto['PrecoTot']))

            # Adiciona cada item na nova linha e na coluna correta
            self.tabCarrinho.setItem(linhasCount, 0, codigo)
            self.tabCarrinho.setItem(linhasCount, 1, nome)
            self.tabCarrinho.setItem(linhasCount, 2, quant)
            self.tabCarrinho.setItem(linhasCount, 3, precoUnit)
            self.tabCarrinho.setItem(linhasCount, 4, precoTot)

        else:
            pass

    def Limpar_Carrinho(self):
        # Limpa todo o conteúdo da tabela
        self.tabCarrinho.clearContents()

        # Remove todas as colunas
        self.tabCarrinho.setRowCount(0)

    def Concluir_Compra(self):
        lista_Compra = []
        for linha in range(self.tabCarrinho.rowCount()):
            produto = []
            for coluna in range(0, 5):
                item = self.tabCarrinho.item(linha, coluna)
                produto.append(item.text())
            lista_Compra.append(produto)
        print(lista_Compra)

        lista_Compra = []
        for linha in range(self.tabCarrinho.rowCount()):
            codigo = int(self.tabCarrinho.item(linha, 0).item())
            nome = self.tabCarrinho.item(linha, 1).item()
            quant = int(self.tabCarrinho.item(linha, 2).item())
            valorTot = int(self.tabCarrinho.item(linha, 4).item())

            # Remover da DB Estoque
            # UPDATE estoque

            # Adicionar na DB Historic
            # INSERT INTO historico (codigo, nome, data, quant, valorTot)
            # VALUES (codigo, nome, NOW(), quant, valorTOT)

    def Remover_Item(self):
        # Busca a linha atual
        linhaAtual = self.tabCarrinho.currentRow()

        # Remove a linha
        self.tabCarrinho.removeRow(linhaAtual)

        # Coloca a célula selecionada em nada
        self.tabCarrinho.setCurrentCell(-1, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = App()
    janela.show()
    app.exec()
