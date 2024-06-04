# main.py
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QDateTime,QTimer
from PyQt5 import QtWidgets,uic,QtCore
from PyQt5.QtWidgets import QMainWindow,QTableWidget,QShortcut,QLineEdit,QTableWidgetItem,QLabel
from janela import janelaFechamento,JanelaProdutocomsulta,janelaproduto,janelaNotas
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut,QLineEdit,QTableWidgetItem,QLabel
from PyQt5.QtCore import pyqtSignal
import mysql.connector
import time

print('programa capixaba')

class Produto:
    def __init__(self, nome, quantidade, preco):    
        self.nome = nome
        self.quantidade = quantidade
        self.preco = float(preco.replace('R$', '').replace(',', '.'))  # Extrai o valor numérico
        self.subtotal = round(float(self.preco) * float(self.quantidade), 3)


class minhaBiblioteca:
    def __init__(self): 
        self.produtos = []

    def adicionar_produto(self, nome, quantidade, preco):
        produto = Produto(nome, quantidade, preco)
        self.produtos.append(produto)

    def obter_total(self):
        # Corrigir a referência ao subtotal na soma
        return sum(produto.subtotal for produto in self.produtos)
    



class WorkerThread(QThread):
    resultados_obtidos = pyqtSignal(list)
    
    def __init__(self, pagina_principal, codigo_produto, quantidade_produto, minha_biblioteca):
        super().__init__()
        self.pagina_principal = pagina_principal
        self.codigo_produto = codigo_produto
        self.quantidade_produto = quantidade_produto
        self.minha_biblioteca = minha_biblioteca

    def run(self):
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                database='meubanco'
            )

            cursor = conexao.cursor()

            consulta = "SELECT nome, preco FROM produtos WHERE codigo = %s"
            cursor.execute(consulta, (self.codigo_produto,))

            resultados = cursor.fetchall()

            lista_produtos = []

            if resultados:
                for row, resultado in enumerate(resultados):
                    nome_produto, preco_produto = resultado
                    quantidade_formatada = "{:.3f}".format(float(self.quantidade_produto))
                    preco_formatado = "R$ {:.2f}".format(float(preco_produto))

                    self.minha_biblioteca.adicionar_produto(nome_produto, quantidade_formatada, preco_formatado)

                    self.pagina_principal.tableWidget.insertRow(row)
                    self.pagina_principal.tableWidget.setItem(row, 0, QTableWidgetItem(nome_produto))
                    self.pagina_principal.tableWidget.setItem(row, 1, QTableWidgetItem(quantidade_formatada))
                    self.pagina_principal.tableWidget.setItem(row, 2, QTableWidgetItem(preco_formatado))

                    subtotal = round(float(preco_produto) * float(self.quantidade_produto), 3)
                    subtotal_formatado = "R$ {:.2f}".format(subtotal)
                    self.pagina_principal.tableWidget.setItem(row, 3, QTableWidgetItem(str(subtotal_formatado)))

                    produto = {
                        'nome': nome_produto,
                        'quantidade': self.quantidade_produto,
                        'preco': preco_produto,
                        'subtotal': subtotal
                    }
                    lista_produtos.append(produto)
                    self.resultados_obtidos.emit(lista_produtos)
                    
                    self.pagina_principal.tableWidget.setItem(row, 3, QTableWidgetItem(str(subtotal_formatado)))
                    
                    self.totalfinal_formatado = "R${:.2f}".format(self.minha_biblioteca.obter_total())
                    self.pagina_principal.total.setText(str(self.totalfinal_formatado))

                self.pagina_principal.tableWidget.setColumnWidth(0, 250)
                self.pagina_principal.tableWidget.setColumnWidth(1, 140)
                self.pagina_principal.tableWidget.setColumnWidth(2, 150)
                self.pagina_principal.tableWidget.setColumnWidth(3, 150)

                print("Dados exibidos na tabela.")
            else:
                print("Produto não encontrado.")
                self.pagina_principal.mostra_frame()
                

        except mysql.connector.Error as err:
            print(f"Erro no banco de dados: {err}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

            self.finished.emit()
            
    
         
        

class PaginaPrincipal(QtWidgets.QMainWindow):
    sinal_total_venda = pyqtSignal(float)
    sinal_codigo = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        uic.loadUi("pagina_principal.ui", self)  # Carrega a interface da página principal
        self.erro.hide()
        self.lista_produtos = []
        self.minha_biblioteca = minhaBiblioteca()
        self.nome_usuario = ""

        
        
        self.peso.installEventFilter(self) # Conecte o evento keyPressEvent ao QLineEdit de quantidade
        self.data = self.findChild(QLabel,'data')
        self.hora = self.findChild(QLabel,'hora')
        self.timer = QTimer(self)
        self.id_venda = self.findChild(QLabel, "id")
        self.timer.timeout.connect(self.atualizar_data_hora)
        self.timer.start(1000)
        
        self.produto = self.findChild(QLineEdit,"produto")
        self.peso = self.findChild(QLineEdit,"peso")
        self.peso.setText("1,000")
        
        f8_shortcut = QShortcut(Qt.Key_F8, self)
        f8_shortcut.activated.connect(self.abrir_pesquisa_f8)
        
        f2_shortcut = QShortcut(Qt.Key_F2,self)
        f2_shortcut.activated.connect(self.abri_janelaNotas)
            
        f12_shortcut =QShortcut(QKeySequence(Qt.Key_F12),self)
        f12_shortcut.activated.connect(self.abri_fechamento)
    
        f4_shortcut = QShortcut(QKeySequence(Qt.Key_F4),self)
        f4_shortcut.activated.connect(self.abri_pesquisa)
        
        f5_shortcut = QShortcut(QKeySequence(Qt.Key_F5), self)
        f5_shortcut.activated.connect(self.abrir_Cancelamento)
        
        atalho_enter = QShortcut(QKeySequence(Qt.Key_Return), self)
        atalho_enter.activated.connect(self.receber_dados)
        
        atalho_enter_num = QShortcut(QKeySequence(Qt.Key_Enter  ),self)
        atalho_enter_num.activated.connect(self.receber_dados)
        

        self.conexao_banco = mysql.connector.connect(
            host='localhost',
            user='root',
            database='meubanco'
        )


    def mostra_frame(self):
        self.erro.show()
        self.erro_line.setFocus()
        time.sleep(3)
        self.erro.hide()

  
    def abrir_Cancelamento(self):
        # Criação e carregamento da janela de cancelamento
        self.janela_cancelamento = QtWidgets.QMainWindow()
        uic.loadUi("cancelamento.ui", self.janela_cancelamento)

        # Encontrar o widget 'senha' na janela de cancelamento
        senha_cancelamento = self.janela_cancelamento.findChild(QLineEdit, "senha")

        if senha_cancelamento:
            # Conectar o evento 'returnPressed' à função específica da janela de cancelamento
            senha_cancelamento.returnPressed.connect(self.validar_usuario_cancelamento)
        else:
            print("Widget 'senha' não encontrado em 'cancelamento.ui'!")

        self.janela_cancelamento.show()

    def validar_usuario_cancelamento(self):
        # Função de validação específica para a janela de cancelamento
        nome_usuario = self.janela_cancelamento.findChild(QLineEdit,"usuario").text()  # Corrija para o nome do widget correto
        senha = self.janela_cancelamento.findChild(QLineEdit, "senha").text()

        cursor = self.conexao_banco.cursor()
        query = f"SELECT * FROM usuarios WHERE nome = '{nome_usuario}' AND senha = '{senha}'"

        cursor.execute(query)
        resultado = cursor.fetchone()

        if resultado:
            # Usuário e senha válidos
            print("Login bem-sucedido na janela de cancelamento!!!!!")
            self.remover_item()
            self.janela_cancelamento.close()
        else:
            # Usuário ou senha inválidos
            print("Login falhou na janela de cancelamento. Verifique suas credenciais.")

        cursor.close()

    def atualizar_tabela(self, lista_produtos):
        for row, produto in enumerate(lista_produtos):
            # Adicione as linhas à tabela conforme necessário
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(produto['nome']))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(produto['quantidade'])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem("R$ {:.2f}".format(produto['preco'])))
            self.tableWidget.setItem(row, 3, QTableWidgetItem("R$ {:.2f}".format(produto['subtotal'])))
        
        # Atualize o total
        self.atualizar_total()
    
    def limpar_biblioteca(self):
        self.minha_biblioteca.produtos = []
        self.tableWidget.setRowCount(0)  # Limpa a tabela
        self.atualizar_total()  # Atualiza o total para refletir a remoção dos itens

        
    def remover_item(self):
        # Obtém a linha selecionada
        selected_row = self.tableWidget.currentRow()

        # Verifica se uma linha está selecionada
        if selected_row >= 0:
            # Obtém o nome do produto da célula na coluna 0 da linha selecionada
            nome_produto = self.tableWidget.item(selected_row, 0).text()

            # Remove o produto da minha_biblioteca
            for produto in self.minha_biblioteca.produtos:
                if produto.nome == nome_produto:
                    self.minha_biblioteca.produtos.remove(produto)
                    break

            # Remove a linha da tabela
            self.tableWidget.removeRow(selected_row)

            # Atualiza o total e a interface gráfica
            self.atualizar_total()

     
    
    def atualizar_total(self):
        self.totalfinal_formatado = "R${:.2f}".format(self.minha_biblioteca.obter_total())
        self.total.setText(str(self.totalfinal_formatado))
        self.sinal_total_venda.emit(float(self.minha_biblioteca.obter_total()))
        
                   
    
    def atualizar_data_hora(self):
        data_hora_atual = QDateTime.currentDateTime() #obter a data e hora atuais 
        
        formata_data = "yyyy-MM-dd" #formato ano-mes-dia
        formata_hora = "hh:mm:ss"   # formao hora-minuto-segundo
        data_formatada = data_hora_atual.toString(formata_data)
        hora_formatada = data_hora_atual.toString(formata_hora)
        
        self.data.setText(f"data: {data_formatada}")
        self.hora.setText(f"hora: {hora_formatada}")
        
    def eventFilter(self, obj, event):
        if obj is self.peso and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Tab:
                # Se a tecla Tab for pressionada, mova o foco para o QLineEdit de produtos
                self.produto.setFocus()
                return True  # Indique que o evento foi manipulado

        return super().eventFilter(obj, event)
            
    def receber_dados(self, codigo=None):
        print('codigo recebido main.py', codigo)

        # Se o código não foi fornecido, obtê-lo do QLineEdit
        if codigo is None:
            codigo_produto = self.produto.text()
        else:
            codigo_produto = codigo

        # Verifica se o campo de produto está vazio
        if not codigo_produto:
            print("Campo de produto vazio.")
            return

    # Verifica se o campo de peso está vazio
        quantidade_produto = self.peso.text()
        if not quantidade_produto:
            print("Campo de peso vazio.")
            return


        if ',' in quantidade_produto:
            try:
                quantidade_produto = float(quantidade_produto.replace(',', '.'))
            except ValueError:
                print("Quantidade inválida.")
                return
        else:
            try:
                quantidade_produto = int(quantidade_produto)
            except ValueError:
                print("Quantidade inválida.")
                return

        self.worker_thread = WorkerThread(self, codigo_produto, quantidade_produto ,self.minha_biblioteca)
        self.worker_thread.start()
        self.produto.setText("")
        self.produto.setFocus()
        self.peso.setText("1,000")
        
    def abri_janelaNotas(self):
        self.janela_Notas = janelaNotas()
        self.janela_Notas.show()

    def atualizar_interface(self):
        self.tableWidget.repaint()
        print("Interface atualizada.")
       
    def interface(self, produto, peso):
        print(f'produto: {produto}, peso: {peso}')
            
    def abri_pesquisa(self):
        self.janela_produtocomsult = JanelaProdutocomsulta()
        self.janela_produtocomsult.show()
        
    def abrir_pesquisa_f8(self):
        self.janela_procura_f8 = janelaproduto()
        self.janela_procura_f8.emitir_codigo.connect(self.receber_dados)
        self.janela_procura_f8.show()
    
    def receber_codigo(self,codigo):
        print('codigo recebido ',codigo)
        self.receber_dados(codigo)
        
        
    def abri_fechamento(self):
        self.janela_fechamento = janelaFechamento(self.nome_usuario, self)
        with open('exemplo.txt', 'w') as arquivo:
    # Nada precisa ser escrito aqui, pois o arquivo já foi truncado
            pass
        # Adiciona a lista de produtos no arquivo
        with open('exemplo.txt', 'a') as arquivo:
            for produto in self.minha_biblioteca.produtos:
                linha = f"{produto.nome} | {produto.quantidade} | {produto.preco} | {produto.subtotal}\n"
                arquivo.write(linha)
        self.janela_fechamento.show()

    
    
        
# Classe para a janla de login
class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, minha_biblioteca):
        super().__init__()
        uic.loadUi("pro_caixa_logi.ui", self)  # Carrega a interface de login
        self.nome_usuario = ""
        self.minha_biblioteca = minha_biblioteca
        
        self.conexao_banco = mysql.connector.connect(
            host = 'localhost',
            user ='root',
            database = 'meubanco'
        )

        # Conecta a função fucao_principal ao botão de login
        self.pushButton.clicked.connect(self.fucao_principal)
        # Define o botão de login como o botão padrão (para acionar com Enter)
        self.pushButton.setDefault(True)
        # Adiciona um atalho de teclado para o botão de login (Enter)
        enter_shortcut = QShortcut(Qt.Key_Return, self)
        enter_shortcut.activated.connect(self.fucao_principal)
        
        self.minha_biblioteca = minha_biblioteca
        
    def fucao_principal(self):
        
        nome = self.lineEdit.text()
        senha = self.lineEdit_2.text()
        consulta = f"SELECT * FROM usuarios WHERE nome = '{nome}' AND senha = '{senha}'"
        
        try:
            with self.conexao_banco.cursor() as cursor:
                cursor.execute(consulta)
                resultado = cursor.fetchone()

            if resultado:
                print("login bem_sucedido!")
                self.open_pagina_principal(nome)
    
            else:
                print("credenciais inválidas")
                

        except mysql.connector.Error as err:
                # Trate qualquer erro que ocorra durante a execução da consulta
                print(f"Erro no banco de dados: {err}")

      
    def open_pagina_principal(self,nome_usuario):
        self.nome_usuario = nome_usuario
        self.close()  # Fecha a janela de login
        self.pagina_principal = PaginaPrincipal()  # Cria uma instância da janela principal
        self.pagina_principal.nome_usuario = nome_usuario
        self.pagina_principal.usuario.setText(self.nome_usuario)  # Passa o nome do usuário
        self.pagina_principal.show()  # Exibe a janela principal
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    minha_biblioteca = minhaBiblioteca()
    login_window = LoginWindow(minha_biblioteca)
    login_window.show()
    
    sys.exit(app.exec_())
