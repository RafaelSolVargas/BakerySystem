from PyQt5.QtWidgets import QMainWindow
from designs.designLogin import Ui_LoginWindow
from conexoes import Verificar_User
from adm import Adm


class Login(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()  # Chama o construtor padrão da biblioteca PyQT5
        super().setupUi(self)  # Chama o construtor setupUi do design.py

        # Se o botão cancelar for apertado, ativa a função para fechar essa tela
        self.btnLoginCancelar.clicked.connect(self.Fechar)
        # Se o botão Login for apertado, ativa a função para verificar se dá para fazer Login
        self.btnLogingLogin.clicked.connect(self.Abrir_Adm)

        # NOTA IMPORTANTE: Para charmarmos métodos de classe (nativos ou não) de dentro do construtor, não usamos ()
        # Mas para chamar métodos de classe de dentro de outros métodos de classe, usaremos os ()

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
