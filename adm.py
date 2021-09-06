from conexoes import *
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from designs.designAdm import Ui_AdmWindow

historico = ['Código', 'Nome', 'Data', 'Quantidade', 'Valor Total']
estoque = ['Código', 'Nome', 'Quantidade', 'Preço Unitário']

class Adm(QMainWindow, Ui_AdmWindow):
    def __init__(self):
        super().__init__()  # Chama o construtor padrão da biblioteca PyQT5
        super().setupUi(self)  # Chama o construtor setupUi do design.py

        # Conexão dos botões da tela do ADM com suas respectivas funções
        self.btnAdmCadastrar.clicked.connect(self.CadastrarProduto)
        self.btnAdmAtualizar.clicked.connect(self.AtualizarProduto)
        self.btnAdmBuscarAtualiozar.clicked.connect(self.BuscarProduto)
        self.btnAdmAdicionarUser.clicked.connect(self.CadastrarUser)
        self.btnAdmHistorico.clicked.connect(self.BuscarHistorico)
        self.btnAdmEstoque.clicked.connect(self.BuscarEstoque)

    def CadastrarProduto(self):
        codigo = self.txtAdmCodCadastrar.text()
        nome = self.txtAdmNomeCadastrar.text()
        preco = self.txtAdmPrecoCadastrar.text()
        quantidade = self.txtAdmQuantCadastrar.text()

        if codigo != '' and nome != '' and quantidade != '' and preco != '0,00':
            try:
                codigo = int(codigo)
                preco = float(preco.replace(',','.'))
                quantidade = int(quantidade)

                Cadastrar_Produto(codigo, nome, preco, quantidade)

                self.txtAdmMessage.setText("PRODUTO CADASTRADO")
            except:
                self.txtAdmMessage.setText("DADOS INVÁLIDOS")

        self.txtAdmCodCadastrar.clear()
        self.txtAdmNomeCadastrar.clear()
        self.txtAdmPrecoCadastrar.clear()
        self.txtAdmQuantCadastrar.clear()

    def AtualizarProduto(self):
        codigo = self.txtAdmCodAtualizar.text()
        nome = self.txtAdmNomeAtualizar.text()
        preco = self.txtAdmPrecoAtualizar.text()
        quantidade = self.txtAdmQuantAtualizar.text()

        if codigo != '' and nome != '' and quantidade != '' and preco != '0,00':
            try:
                codigo = int(codigo)
                preco = float(preco.replace(',','.'))
                quantidade = int(quantidade)

                Atualizar_Produto(codigo, nome, preco, quantidade)

                self.txtAdmNomeAtualizar.setEnabled(False)
                self.txtAdmNomeAtualizar.clear()

                self.txtAdmPrecoAtualizar.setEnabled(False)
                self.txtAdmPrecoAtualizar.clear()

                self.txtAdmQuantAtualizar.setEnabled(False)
                self.txtAdmQuantAtualizar.clear()

                self.btnAdmAtualizar.setEnabled(False)
                self.txtAdmCodAtualizar.clear()

                self.txtAdmMessage.setText("INFORMAÇÕES DO PRODUTO ATUALIZADAS")
            except:
                self.txtAdmMessage.setText("DADOS INVÁLIDOS")

    def BuscarProduto(self):
        codigo = self.txtAdmCodAtualizar.text()

        if codigo != '':
            try:
                codigo = int(codigo)

                dados = Buscar_Produto(codigo)

                self.txtAdmNomeAtualizar.setEnabled(True)
                self.txtAdmNomeAtualizar.setText(str(dados[1]))

                self.txtAdmPrecoAtualizar.setEnabled(True)
                self.txtAdmPrecoAtualizar.setValue(float(dados[3]))

                self.txtAdmQuantAtualizar.setEnabled(True)
                self.txtAdmQuantAtualizar.setValue(int(dados[2]))

                self.btnAdmAtualizar.setEnabled(True)
            except:
                self.txtAdmMessage.setText("CÓDIGO INVÁLIDO")

    def CadastrarUser(self):
        login = self.txtAdmLogin.text()
        senha = self.txtAdmSenha.text()

        if login != '' and senha != '':
           Cadastrar_User(login, senha)
           self.txtAdmLogin.clear()
           self.txtAdmSenha.clear()
           self.txtAdmMessage.setText("USUÁRIO CADASTRADO COM SUCESSO")
        else:
            self.txtAdmMessage.setText("USUÁRIO OU SENHA INVÁLIDOS")

    def BuscarHistorico(self):
        self.tabAdmTabela.clearContents()
        self.tabAdmTabela.setRowCount(0)

        self.tabAdmTabela.setColumnCount(len(historico))
        self.tabAdmTabela.setHorizontalHeaderLabels(historico)

        hist = Buscar_Historico()

        for i in hist:
            linhasCount = self.tabAdmTabela.rowCount()
            self.tabAdmTabela.insertRow(linhasCount)

            codigoQT = QTableWidgetItem(str(i[1]))
            nomeQT = QTableWidgetItem(i[2])
            dataQT = QTableWidgetItem(i[3])
            quantQT = QTableWidgetItem(str(i[4]))
            totalQT = QTableWidgetItem("R$" + str(round(i[5]*int(i[4]), 2)))

            self.tabAdmTabela.setItem(linhasCount, 0, codigoQT)
            self.tabAdmTabela.setItem(linhasCount, 1, nomeQT)
            self.tabAdmTabela.setItem(linhasCount, 2, dataQT)
            self.tabAdmTabela.setItem(linhasCount, 3, quantQT)
            self.tabAdmTabela.setItem(linhasCount, 4, totalQT)

        self.txtAdmMessage.setText("HISTÓRICO DE COMPRAS:")

    def BuscarEstoque(self):
       self.tabAdmTabela.clearContents()
       self.tabAdmTabela.setRowCount(0)

       self.tabAdmTabela.setColumnCount(len(estoque))
       self.tabAdmTabela.setHorizontalHeaderLabels(estoque)

       est = Buscar_Estoque()
       
       for i in est:
            linhasCount = self.tabAdmTabela.rowCount()
            self.tabAdmTabela.insertRow(linhasCount)

            codigoQT = QTableWidgetItem(str(i[0]))
            nomeQT = QTableWidgetItem(i[1])
            quantQT = QTableWidgetItem(str(i[2]))
            precoQT = QTableWidgetItem(("R$" + str(i[3])))

            self.tabAdmTabela.setItem(linhasCount, 0, codigoQT)
            self.tabAdmTabela.setItem(linhasCount, 1, nomeQT)
            self.tabAdmTabela.setItem(linhasCount, 2, quantQT)
            self.tabAdmTabela.setItem(linhasCount, 3, precoQT)

       self.txtAdmMessage.setText("DADOS DO ESTOQUE:")