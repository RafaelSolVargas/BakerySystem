from conexoes import *
from PyQt5.QtWidgets import QMainWindow
from designs.designAdm import Ui_AdmWindow


class Adm(QMainWindow, Ui_AdmWindow):
    def __init__(self):
        super().__init__()  # Chama o construtor padrão da biblioteca PyQT5
        super().setupUi(self)  # Chama o construtor setupUi do design.py

        # Conexão dos botões da tela do ADM com suas respectivas funções
        self.btnAdmCadastrar.clicked.connect(self.Cadastrar_Produto)
        self.btnAdmAtualizar.clicked.connect(self.Atualizar_Produto)
        self.btnAdmBuscarAtualiozar.clicked.connect(self.Buscar_Produto)
        self.btnAdmAdicionarUser.clicked.connect(self.Cadastrar_User)
        self.btnAdmHistorico.clicked.connect(self.Buscar_Historico)
        self.btnAdmEstoque.clicked.connect(self.Buscar_Estoque)