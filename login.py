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

    def Verificar(self):
        login = self.txtLoginLogin.text()
        senha = self.txtLoginSenha.text()

        if Verificar_User(login, senha):
            self.Abrir_Adm()
        else:
            self.txtLoginMessage.setText("Senha ou Login inválido")

    def Abrir_Adm(self):
        self.Fechar()
        self.admWindow = Adm()
        self.admWindow.show()

    def Fechar(self):
        self.close()
