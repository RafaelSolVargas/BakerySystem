import sys  # Importando bibliotecas externas
# Importando bibliotecas externas
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem

# Importando funções de outros arquivos e o design das abas
from conexoes import *
from login import Login
from designs.designMain import Ui_MainWindow


titulos = ['Código', 'Nome', 'Quantidade', 'Preço Unitário', 'Preço Total']
cache = []


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
        self.txtMainMessage.setText("")

        codigo = self.txtMainCod.text()
        quant = self.txtMainQuant.text()

        if codigo == "" or quant == "":
            self.txtMainMessage.setText(
                "DADOS INCOMPLETOS, COLOQUE ALGO")
            return

        try:
            quant = int(quant)
            codigo = int(codigo)
        except:
            self.txtMainMessage.setText(
                "DADOS INVÁLIDOS")
            return

        in_Cache = False
        compra_Valida = True

        # Procura o item no cache
        for produto in cache:
            if produto[0] == codigo:
                if quant <= produto[1]:
                    produto[1] -= quant
                    in_Cache = True
                else:
                    compra_Valida = False
                break

        # Caso contrário, verifica se o item está presente no banco de dados
        if Verificar_Codigo(codigo, quant) and compra_Valida:
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
            precoUnitQT = QTableWidgetItem(
                "R$ " + str(f'{produto[2]:.2f}').replace('.', ','))
            precoTotQT = QTableWidgetItem(
                "R$ " + str(f'{produto[2]*int(quant):.2f}').replace('.', ','))

            if not in_Cache:
                cache.append([codigo, produto[3]-quant])

            # Adiciona cada item na nova linha e na coluna correta
            self.tabCarrinho.setItem(linhasCount, 0, codigoQT)
            self.tabCarrinho.setItem(linhasCount, 1, nomeQT)
            self.tabCarrinho.setItem(linhasCount, 2, quantQT)
            self.tabCarrinho.setItem(linhasCount, 3, precoUnitQT)
            self.tabCarrinho.setItem(linhasCount, 4, precoTotQT)

        else:
            compra_Valida = False

        if not compra_Valida:
            self.txtMainCod.setText("")
            self.txtMainQuant.clear()
            self.txtMainMessage.setText(
                "CÓDIGO INVÁLIDO OU QUANTIDADE EXCEDENTE")

    def Limpar_Carrinho(self):
        self.tabCarrinho.clearContents()
        self.tabCarrinho.setRowCount(0)
        cache.clear()
        self.txtMainMessage.setText(
            "CARRINHO LIMPO")

    def Concluir_Compra(self):
        # Verifica logo de início se tem algo alguma compra acontecendo
        if self.tabCarrinho.rowCount() == 0:
            self.txtMainMessage.setText(
                "NÃO HÁ COMPRA PARA CONCLUIR")
            return

        # Preenche um array com a lista de compra
        lista_Compra = []
        totalCompra = 0
        for linha in range(self.tabCarrinho.rowCount()):
            produto = []

            # Construindo a lista da compra
            for coluna in range(0, 5):
                item = self.tabCarrinho.item(linha, coluna).text()
                item = item.replace(',', '.').replace('R$', '')
                produto.append(item)
            lista_Compra.append(produto)

            # Fazendo o cálculo do total da compra
            totalProd = self.tabCarrinho.item(linha, 4).text()
            totalProd = totalProd.replace(',', '.').replace('R$', '')
            totalCompra += (float(item))

        # Retorna ao cliente o valor total gasto com a compra
        self.txtMainMessage.setText(
            "COMPRA FINALIZADA! TOTAL DA COMPRA: R$ {:.2f}".format(totalCompra))

        # Chama as funções para atualizar o estoque e o histórico de compras
        Remover_Estoque(lista_Compra)
        Add_Historico(lista_Compra)

        # Reseta o sistema para uma nova compra
        self.txtMainCod.clear()
        self.txtMainQuant.clear()
        self.tabCarrinho.clearContents()
        self.tabCarrinho.setRowCount(0)
        cache.clear()

    def Remover_Item(self):
        # Busca a linha atual
        linhaAtual = self.tabCarrinho.currentRow()

        if linhaAtual == -1:
            self.txtMainMessage.setText('NENHUMA LINHA SELECIONADA')
            return

        # Adiciona o valor de estoque previamente tirado do cache de volta ao mesmo
        itemCodigo = self.tabCarrinho.item(linhaAtual, 0).text()
        itemQuant = self.tabCarrinho.item(linhaAtual, 2).text()

        for produto in cache:
            if int(itemCodigo) in produto:
                produto[1] += int(itemQuant)

        # Remove a linha
        self.tabCarrinho.removeRow(linhaAtual)
        # Coloca a célula selecionada em nada
        self.tabCarrinho.setCurrentCell(-1, 0)
        self.txtMainMessage.setText(
            "ITEM REMOVIDO COM SUCESSO")

    def Mostrar_Login(self):
        # Cria um novo objeto com a classe Login
        self.loginWindow = Login()
        self.loginWindow.show()  # E mostra ele na tela


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = Main()
    janela.show()
    app.exec()
