from PyQt5.QtWidgets import QMainWindow
from designs.designLogin import Ui_LoginWindow
from conexoes import Verificar_User
from adm import Adm


class Login(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()  # Chama o construtor padrão da biblioteca PyQT5
        super().setupUi(self)  # Chama o construtor setupUi do design.py

        self.btnLoginCancelar.clicked.connect(self.Fechar)
        self.btnLogingLogin.clicked.connect(self.Verificar)

    # Função para verificar se o login e senha batem
    def Verificar(self):
        login = self.txtLoginLogin.text()  # Puxa texto do label login
        senha = self.txtLoginSenha.text()  # Puxa texto do label senha

        # Chama a função de conexão para verificar se existe o usuário no DB
        if Verificar_User(login, senha):
            self.Abrir_Adm()  # Se sim chama a função para Abrir_Adm
        else:
            self.txtLoginMessage.setText("Dados inválidos")

    # Função para fechar essa tela e abrir a ADM
    def Abrir_Adm(self):
        self.Fechar()
        self.admWindow = Adm()
        self.admWindow.show()

    # Fecha essa tela
    def Fechar(self):
        self.close()
