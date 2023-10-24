# janelas.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QShortcut
from PyQt5.QtGui import QKeySequence

from PyQt5 import QtWidgets, uic

class JanelaCancelar(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__()
        uic.loadUi("cancelamento.ui", self)

class JanelaPordutos(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("botao_f8.ui", self)
        
        # Adicione um widget de interface de usuário para pesquisa
        self.search_input = self.findChild(QLineEdit, "lineEdit_codigo")

        # Conecte a tecla Enter ao slot de pesquisa
        enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        enter_shortcut.activated.connect(self.search_product)

        # Suponhamos que você tenha uma lista de produtos para pesquisa
        self.product_list = [
            {"codigo": "001", "nome": "Produto 1"},
            {"codigo": "002", "nome": "Produto 2"},
            # Adicione mais produtos aqui
        ]

    def search_product(self):
        # Obtenha o texto de pesquisa do campo de entrada
        search_text = self.search_input.text().strip()

        # Realize a pesquisa
        results = self.perform_search(search_text)

        # Exiba os resultados na interface do usuário
        self.display_results(results)

    def perform_search(self, search_text):
        # Implemente a lógica de pesquisa aqui
        # Por exemplo, percorra a lista de produtos e verifique se o código contém o texto de pesquisa
        results = []
        for product in self.product_list:
            if search_text.lower() in product["codigo"].lower():
                results.append(product)
        return results

    def display_results(self, results):
        # Implemente como você deseja exibir os resultados na interface do usuário
        # Pode ser uma tabela, uma lista, etc.
        pass
class JanelafechaVenda(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("fechaVenda.ui", self)