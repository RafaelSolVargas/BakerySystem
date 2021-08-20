# Importar a classe da GUI feita no PyQT5

# Instanciar a nossa classe

import sys
from design2 import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.btnRemover.clicked.connect(self.Remover_Item)
        self.btnLimpar.clicked.connect(self.Limpar_Carrinho)

    def Verifica_Cod(self):
        pass

    def Add_Carrinho(self):
        # Descobre a quantidade de linhas na tabela
        linhasCount = self.tabCarrinho.rowCount()
        # Adiciona uma nova linha, por meio do index dela
        self.tabCarrinho.insertRow(linhasCount)

        # Cria as variáveis dos itens para adicionar na nova linha
        codigo = QTableWidgetItem(str(novoProduto['Codigo']))
        nome = QTableWidgetItem(novoProduto['Nome'])
        quant = QTableWidgetItem(str(novoProduto['Quant']))
        precoUnit = QTableWidgetItem(str(novoProduto['PrecoUnit']))
        precoTot = QTableWidgetItem(str(novoProduto['PrecoTot']))

        # Adiciona cada item na nova linha e na coluna correta
        self.tabCarrinho.setItem(linhasCount, 0, codigo)
        self.tabCarrinho.setItem(linhasCount, 1, nome)
        self.tabCarrinho.setItem(linhasCount, 2, quant)
        self.tabCarrinho.setItem(linhasCount, 3, precoUnit)
        self.tabCarrinho.setItem(linhasCount, 4, precoTot)

    def Limpar_Carrinho(self):
        self.tabCarrinho.clearContents()
        self.tabCarrinho.setRowCount(0)
        pass

    def Concluir_Compra(self):
        pass

    def Acessar_Adm(self):
        pass

    def Remover_Item(self):
        linhaAtual = self.tabCarrinho.currentRow()
        self.tabCarrinho.removeRow(linhaAtual)
        pass

    def Conectar_Banco(self):
        # Deve retornar uma estrutura com o codigo, nome, quant, precoUnit, precoTot
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = App()
    janela.show()
    app.exec()
