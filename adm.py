from conexoes import *
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from designs.designAdm import Ui_AdmWindow

historicoTitulos = ['Código', 'Nome', 'Data', 'Quantidade', 'Valor Total']
estoqueTitulos = ['Código', 'Nome', 'Quantidade', 'Preço Unitário']


class Adm(QMainWindow, Ui_AdmWindow):
    def __init__(self):
        super().__init__()  # Chama o construtor padrão da biblioteca PyQT5
        super().setupUi(self)  # Chama o construtor setupUi do design.py

        # Conexão dos botões da tela do ADM com suas respectivas funções
        self.btnAdmCadastrar.clicked.connect(self.CadastrarProduto)
        self.btnAdmAtualizar.clicked.connect(self.AtualizarProduto)
        self.btnAdmBuscarAtualizar.clicked.connect(self.BuscarProduto)
        self.btnAdmAdicionarUser.clicked.connect(self.CadastrarUser)
        self.btnAdmHistorico.clicked.connect(self.BuscarHistorico)
        self.btnAdmEstoque.clicked.connect(self.BuscarEstoque)

    def CadastrarProduto(self):
        codigo = self.txtAdmCodCadastrar.text()
        nome = self.txtAdmNomeCadastrar.text()
        preco = self.txtAdmPrecoCadastrar.text()
        quantidade = self.txtAdmQuantCadastrar.text()

        if codigo != '' and nome != '' and quantidade != '' and preco != '0,00':
            if len(codigo) == 5:
                if codigo[0] != 0:
                    try:
                        # Só tenta transformar para inteiro, sem interferir no tipo de dado do código
                        codigo2 = int(codigo)
                        # para que caso o código comece com 0 não perca o valor, note que o valor não é enviado ao bd
                        preco = float(preco.replace(',', '.'))
                        quantidade = int(quantidade)

                        Cadastrar_Produto(codigo, nome, preco, quantidade)

                        self.txtAdmMessage.setText("PRODUTO CADASTRADO")
                    except:
                        self.txtAdmMessage.setText("DADOS INVÁLIDOS")
                        return
                else:
                    self.txtAdmMessage.setText(
                        'O CÓDIGO NÃO PODE COMEÇAR COM UM ZERO')
                    return
            else:
                self.txtAdmMessage.setText('O CÓDIGO DEVE CONTER 5 DÍGITOS')
                return
        else:
            self.txtAdmMessage.setText('DADOS INCOMPLETOS')
            return

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
                preco = float(preco.replace(',', '.'))
                quantidade = int(quantidade)
            except:
                self.txtAdmMessage.setText("DADOS INVÁLIDOS")
                return
        else:
            self.txtAdmMessage.setText('DADOS INCOMPLETOS')
            return

        Atualizar_Produto(codigo, nome, preco, quantidade)
        self.txtAdmNomeAtualizar.setEnabled(False)
        self.txtAdmNomeAtualizar.clear()

        self.txtAdmPrecoAtualizar.setEnabled(False)
        self.txtAdmPrecoAtualizar.clear()

        self.txtAdmQuantAtualizar.setEnabled(False)
        self.txtAdmQuantAtualizar.clear()

        self.txtAdmCodAtualizar.setEnabled(True)
        self.txtAdmCodAtualizar.clear()

        self.btnAdmAtualizar.setEnabled(False)
        self.btnAdmBuscarAtualizar.setEnabled(True)
        self.txtAdmMessage.setText(
            "INFORMAÇÕES DO PRODUTO ATUALIZADAS")

    def BuscarProduto(self):
        codigo = self.txtAdmCodAtualizar.text()

        if codigo != '':
            if not Verificar_Codigo(codigo, 0):
                self.txtAdmMessage.setText("CÓDIGO INVÁLIDO")
                return
        else:
            self.txtAdmMessage.setText(
                'DIGITE UM CÓDIGO PARA BUSCAR O PRODUTO')
            return

        produto = Buscar_Produto(codigo)

        self.txtAdmNomeAtualizar.setEnabled(True)
        self.txtAdmNomeAtualizar.setText(str(produto[1]))

        self.txtAdmPrecoAtualizar.setEnabled(True)
        self.txtAdmPrecoAtualizar.setValue(float(produto[3]))

        self.txtAdmQuantAtualizar.setEnabled(True)
        self.txtAdmQuantAtualizar.setValue(int(produto[2]))

        self.btnAdmAtualizar.setEnabled(True)
        self.btnAdmBuscarAtualizar.setEnabled(False)
        self.txtAdmCodAtualizar.setEnabled(False)

    def CadastrarUser(self):
        login = self.txtAdmLogin.text()
        senha = self.txtAdmSenha.text()

        if login != '' and senha != '':
            Cadastrar_User(login, senha)
            self.txtAdmLogin.clear()
            self.txtAdmSenha.clear()
            self.txtAdmMessage.setText("USUÁRIO CADASTRADO COM SUCESSO")
        else:
            self.txtAdmMessage.setText(
                "ESCOLHA UM USUÁRIO E UMA SENHA PARA CADASTRAR")

    def BuscarHistorico(self):
        self.tabAdmTabela.clearContents()
        self.tabAdmTabela.setRowCount(0)
        self.tabAdmTabela.setColumnCount(len(historicoTitulos))
        self.tabAdmTabela.setHorizontalHeaderLabels(historicoTitulos)

        historico = Buscar_Historico()

        for produto in historico:
            linhasCount = self.tabAdmTabela.rowCount()
            self.tabAdmTabela.insertRow(linhasCount)

            codigoQT = QTableWidgetItem(str(produto[1]))
            nomeQT = QTableWidgetItem(produto[2])
            dataQT = QTableWidgetItem(produto[3])
            quantQT = QTableWidgetItem(str(produto[4]))
            totalQT = QTableWidgetItem(
                "R$ " + str(f'{produto[5]*int(produto[4]):.2f}').replace('.', ','))

            self.tabAdmTabela.setItem(linhasCount, 0, codigoQT)
            self.tabAdmTabela.setItem(linhasCount, 1, nomeQT)
            self.tabAdmTabela.setItem(linhasCount, 2, dataQT)
            self.tabAdmTabela.setItem(linhasCount, 3, quantQT)
            self.tabAdmTabela.setItem(linhasCount, 4, totalQT)

        self.txtAdmMessage.setText("HISTÓRICO DE VENDAS:")

    def BuscarEstoque(self):
        self.tabAdmTabela.clearContents()
        self.tabAdmTabela.setRowCount(0)

        self.tabAdmTabela.setColumnCount(len(estoqueTitulos))
        self.tabAdmTabela.setHorizontalHeaderLabels(estoqueTitulos)

        estoque = Buscar_Estoque()

        for produto in estoque:
            linhasCount = self.tabAdmTabela.rowCount()
            self.tabAdmTabela.insertRow(linhasCount)

            codigoQT = QTableWidgetItem(str(produto[0]))
            nomeQT = QTableWidgetItem(produto[1])
            quantQT = QTableWidgetItem(str(produto[2]))
            precoQT = QTableWidgetItem(
                "R$ " + str(f'{produto[3]:.2f}').replace('.', ','))

            self.tabAdmTabela.setItem(linhasCount, 0, codigoQT)
            self.tabAdmTabela.setItem(linhasCount, 1, nomeQT)
            self.tabAdmTabela.setItem(linhasCount, 2, quantQT)
            self.tabAdmTabela.setItem(linhasCount, 3, precoQT)

        self.txtAdmMessage.setText("DADOS DO ESTOQUE:")
