# main.py
import sys
from PyQt5 import QtWidgets,uic
from janela import JanelaCancelar, JanelaPordutos, JanelafechaVenda
from banco_dados import adicionar_produto, listar_produtos
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence 
from PyQt5.QtWidgets import QShortcut

# ... Outro código principal ...
class PaginaPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("pagina_principal.ui", self)  # Carrega a interface da página principal

        # Conecta o botão "Cancelar" ao método abrir_cancelamento
        self.f2camadas_2.clicked.connect(self.abrir_cancelamento)
        self.f8_produto.clicked.connect(self.abrir_Produtos)
        self.f2camadas_5.clicked.connect(self.abrir_fechaVenda)
        
        
        f5_shortcut = QShortcut(QKeySequence(Qt.Key_5), self)
        f5_shortcut.activated.connect(self.abrir_cancelamento)
        
        f8_shortcut = QShortcut(QKeySequence(Qt.Key_8), self)
        f8_shortcut.activated.connect(self.abrir_Produtos)

        f10_shortcut =QShortcut(QKeySequence(Qt.Key_0),self)
        f10_shortcut.activated.connect(self.abrir_fechaVenda)
        
    def abrir_cancelamento(self):
        self.janela_cancelamento = JanelaCancelar()
        self.janela_cancelamento.show()
        
        
    def abrir_Produtos(self):
        self.janela_cancelamento = JanelaPordutos()
        self.janela_cancelamento.show()
        
    def abrir_fechaVenda(self):
        self.janela_cancelamento = JanelafechaVenda()
        self.janela_cancelamento.show()
        
    def adicionar_produtos_a_lista(self):
        nome_produto = self.lineEdit.text()
        quantidade = int(self.lineEdit_2.text())
        
        produto_encontrado = None
        for produto in listar_produtos:
            if produto["nome"] == nome_prouto:
                produto_encontrado =produto
                break
        
        if produto_encontrado:
            produto_encontrado["quantidade"] = quantidade
        else:
            novo_produto = {
                "nome": nome_produto,
                "quantidade": quantidade
            }
            lista_de_produtos.append(novo_produto)
        
        listar_produtos()
# Classe para a janela de login
class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("pro_caixa_logi.ui", self)  # Carrega a interface de login

        # Credenciais válidas (substitua por suas próprias credenciais)
        self.credenciais_validas = {
            "usuario": "wesley",
            "senha": "caxiado99"
        }
        
        # Conecta a função fucao_principal ao botão de login
        self.pushButton.clicked.connect(self.fucao_principal)

        # Define o botão de login como o botão padrão (para acionar com Enter)
        self.pushButton.setDefault(True)

        # Adiciona um atalho de teclado para o botão de login (Enter)
        enter_shortcut = QShortcut(Qt.Key_Return, self)
        enter_shortcut.activated.connect(self.fucao_principal)
           
    def fucao_principal(self):
        usuario = self.lineEdit.text()
        senha = self.lineEdit_2.text()
        print(usuario)
        print(senha)

        if usuario == self.credenciais_validas["usuario"] and senha == self.credenciais_validas["senha"]:
            print("Login bem-sucedido!")
            self.open_pagina_principal()
        else:
            print("Credenciais inválidas. Tente novamente.")
    
    def open_pagina_principal(self):
        self.close()  # Fecha a janela de login
        self.pagina_principal = PaginaPrincipal()  # Cria uma instância da janela principal
        self.pagina_principal.show()  # Exibe a janela principal

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
