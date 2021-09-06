import sys  # Importando bibliotecas externas
# Importando bibliotecas externas
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem

# Importando funções de outros arquivos e o design das abas
from conexoes import *
from login import Login
from designs.designMain import Ui_MainWindow


titulos = ['Código', 'Nome', 'Quantidade', 'Preço Unitário', 'Preço Total']


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):  # Construtor do APP
        super().__init__()  # Chama o construtor padrão da biblioteca PyQT5
        super().setupUi(self)  # Chama o construtor setupUi do design.py

        # Adiciona o nome de cada coluna à tabela do carrinho, na ordem do array titulos
        self.tabCarrinho.setColumnCount(len(titulos))
        self.tabCarrinho.setHorizontalHeaderLabels(titulos)

        # Adicionar as conexões intrínsecas a cada botão
        self.btnMainAdicionar.clicked.connect(self.Add_Carrinho)
        self.btnMainRemover.clicked.connect(self.Remover_Item)
        self.btnMainLimpar.clicked.connect(self.Limpar_Carrinho)
        self.btnMainConcluir.clicked.connect(self.Concluir_Compra)
        self.commandLinkButton.clicked.connect(self.Mostrar_Login)

    def Add_Carrinho(self):
        codigo = self.txtMainCod.text()
        quant = self.txtMainQuant.text()

        # ALTERAÇÃO
        if codigo == "" or quant == "":
            self.txtMainMessage.setText(
                "DADOS INCOMPLETOS, COLOQUE ALGO")
            return

        if Verificar_Codigo(codigo, quant):
            # Traz o produto do banco de dados
            produto = Carregar_Produto(codigo)

            # Descobre a quantidade de linhas na tabela
            linhasCount = self.tabCarrinho.rowCount()

            # Adiciona uma nova linha, por meio do index dela
            self.tabCarrinho.insertRow(linhasCount)

            # Cria as variáveis dos itens para adicionar na nova linha
            codigoQT = QTableWidgetItem(str(codigo))
            nomeQT = QTableWidgetItem(produto[1])
            quantQT = QTableWidgetItem(str(quant))
            # precoUnitQT = QTableWidgetItem(str(produto[2]))
            precoUnitQT = QTableWidgetItem(
                "R$ " + str(f'{produto[2]:.2f}').replace('.', ','))
            precoTotQT = QTableWidgetItem(
                "R$ " + str(f'{produto[2]*int(quant):.2f}').replace('.', ','))

            # Adiciona cada item na nova linha e na coluna correta
            self.tabCarrinho.setItem(linhasCount, 0, codigoQT)
            self.tabCarrinho.setItem(linhasCount, 1, nomeQT)
            self.tabCarrinho.setItem(linhasCount, 2, quantQT)
            self.tabCarrinho.setItem(linhasCount, 3, precoUnitQT)
            self.tabCarrinho.setItem(linhasCount, 4, precoTotQT)

        else:
            self.txtMainCod.setText("")
            self.txtMainQuant.clear()
            self.txtMainMessage.setText(
                "CÓDIGO INVÁLIDO OU QUANTIDADE INVÁLIDA")

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

        # Apenas settar a mensagem de erro, as funções não são executadas caso a lista seja vazia
        if lista_Compra == []:
            self.txtMainMessage.setText(
                "CARRINHO VAZIO")

        # Implementar chamada para Atualizar Estoque
        Remover_Estoque(lista_Compra)
        # Implementar chamada para Adicionar venda ao Histórico
        Add_Historico(lista_Compra)

    def Remover_Item(self):
        # Busca a linha atual
        linhaAtual = self.tabCarrinho.currentRow()

        # Remove a linha
        self.tabCarrinho.removeRow(linhaAtual)

        # Coloca a célula selecionada em nada
        self.tabCarrinho.setCurrentCell(-1, 0)

    def Mostrar_Login(self):
        # Cria um novo objeto com a classe Login
        self.loginWindow = Login()
        self.loginWindow.show()  # E mostra ele na tela


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = Main()
    janela.show()
    app.exec()
