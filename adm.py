from conexoes import *
from PyQt5.QtWidgets import QMainWindow
from designs.designAdm import Ui_AdmWindow


class Adm(QMainWindow, Ui_AdmWindow):
    def __init__(self):
        super().__init__()  # Chama o construtor padrão da biblioteca PyQT5
        super().setupUi(self)  # Chama o construtor setupUi do design.py

        ############################
        # Configurar aqui toda a lógica da tela do ADM com os clicked.connect()
