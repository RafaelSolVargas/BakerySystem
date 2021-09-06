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
        codigo = self.txtMainCod.text()
        quant = self.txtMainQuant.text()

        # ALTERAÇÃO
        if codigo == "" or quant == "":
            self.txtMainMessage.setText(
                "DADOS INCOMPLETOS, COLOQUE ALGO")
            return

        quantidade_anterior = 0
        index = 0
        in_cache = False
        pode_add = False

        # Procura o item no cache
        for anterior in cache:
            if int(codigo) in anterior:
                index = cache.index(anterior)
                quantidade_anterior = anterior[1]
                in_cache = True
                break

        # Caso esteja no cache, verifica se tem estoque suficiente
        if in_cache:
            if quantidade_anterior >= int(quant) and quantidade_anterior > 0:
                cache[index][1] -= int(quant)
                pode_add = True

        # Caso contrário, verifica se o item está presente no banco de dados
        else:
            if Verificar_Codigo(codigo, quant):
                pode_add = True

        # Se o item estiver registrado em algum desses lugares, ele é adiocionado ao carrinho
        if pode_add:
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

            # Adiciona cada item na nova linha e na coluna correta
            self.tabCarrinho.setItem(linhasCount, 0, codigoQT)
            self.tabCarrinho.setItem(linhasCount, 1, nomeQT)
            self.tabCarrinho.setItem(linhasCount, 2, quantQT)
            self.tabCarrinho.setItem(linhasCount, 3, precoUnitQT)
            self.tabCarrinho.setItem(linhasCount, 4, precoTotQT)

            # Caso o item não esteja registrado no cache, ele é registrado já com a quantidade descontada
            if not in_cache:
                cache.append([produto[0], (produto[3]-int(quant))])

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

        # Limpa o conteúdo do cache
        cache.clear()

        self.txtMainMessage.setText(
            "CARRINHO LIMPO")

    def Concluir_Compra(self):
        lista_Compra = []
        for linha in range(self.tabCarrinho.rowCount()):
            produto = []
            for coluna in range(0, 5):
                item = self.tabCarrinho.item(linha, coluna)
                item = item.text()
                item = item.replace(',', '.')
                item = item.replace('R$ ', '')
                produto.append(item)
            lista_Compra.append(produto)

        # Cálculo do total da compra
        total = 0
        for linha in range(self.tabCarrinho.rowCount()):
            item = self.tabCarrinho.item(linha, 4)
            item = item.text()
            item = item.replace(',', '.')
            item = item.replace('R$ ', '')
            total += (float(item))

        # Apenas settar a mensagem de erro, as funções não são executadas caso a lista seja vazia
        if lista_Compra == []:
            self.txtMainMessage.setText(
                "CARRINHO VAZIO")
        else:
            self.txtMainMessage.setText(
                "COMPRA FINALIZADA! TOTAL DA COMPRA: R$ {:.2f}".format(total))

        # Implementar chamada para Atualizar Estoque
        Remover_Estoque(lista_Compra)
        # Implementar chamada para Adicionar venda ao Histórico
        Add_Historico(lista_Compra)

        # Limpa as lacunas
        self.txtMainCod.clear()
        self.txtMainQuant.clear()

        # Limpa todo o conteúdo da tabela
        self.tabCarrinho.clearContents()

        # Remove todas as colunas
        self.tabCarrinho.setRowCount(0)

        # Limpa o conteúdo do cache
        cache.clear()

    def Remover_Item(self):
        # Busca a linha atual
        linhaAtual = self.tabCarrinho.currentRow()

        # Adiciona o valor de estoque previamente tirado do cache de volta ao mesmo
        item = self.tabCarrinho.item(linhaAtual, 0)
        item2 = self.tabCarrinho.item(linhaAtual, 2)

        codigo = item.text()
        quant = item2.text()

        for i in cache:
            if int(codigo) in i:
                i[1] += int(quant)

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
