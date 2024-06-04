# janelas.py
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QShortcut, QApplication,QDialog,QTableWidget,QTableWidgetItem, QWidget ,QLabel,QPushButton,QComboBox
from PyQt5.QtGui import QKeySequence, QShowEvent
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5 import uic,QtCore
import mysql.connector


class abaNotasVendas(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("aba_notas_vendas.ui", self)

class janelaFechamento(QMainWindow):
   
    def __init__(self, nome_usuario, pagina_principal):
        super().__init__()
        uic.loadUi("fechaVenda.ui", self)
        
        self.nome_usuario = nome_usuario   # nome do usuário #caixa
        self.pagina_principal = pagina_principal
        self.ID_vendas = self.findChild(QLabel, "id")
        self.labelTotal = self.findChild(QLabel, "label_total")
        self.labeDesconto = self.findChild(QLabel, "labe_desconto")
        self.labeReceber = self.findChild(QLabel, "labe_receber")
        self.receber_max = self.findChild(QLabel, "receber_max")
        self.total_max = self.findChild(QLabel, "total_max")
        self.usuario_1 = self.findChild(QLabel, "usuario_1")  
        self.OBS = self.findChild(QLineEdit, "OBS") 
        self.tipo_pagamento = self.findChild(QLabel, "tipo_pagamento")

        self.botao_fechar_compra = self.findChild(QPushButton, "fechar")
        self.botao_fechar_compra.setAutoDefault(True)
        self.botao_fechar_compra.clicked.connect(self.fechar_compra)

        self.ESC = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.ESC.activated.connect(self.fechar_janela)

        self.receber1 = self.findChild(QLineEdit, "forma_pagamento1")
        self.receber2 = self.findChild(QLineEdit, "forma_pagamento2")
        print(self.receber1)
        print(self.receber2)

        self.receber1.returnPressed.connect(self.atualizar_interface)
        self.receber2.returnPressed.connect(self.atualizar_interface)
        
        self.lista_compras = []  # Inicializando o atributo

        # conectar comboBox de tipo de pagamento 
        self.combo_tipo = self.findChild(QComboBox, "comboBox")
        self.combo_tipo.currentTextChanged.connect(self.atualizar_opcao_selecionada)
   
        self.conectar_carregar_compras()
        
    def showEvent(self, event):
        self.conectar_carregar_compras()
        event.accept()

    def fechar_janela(self):
        self.close()
        
    def atualizar_opcao_selecionada(self, texto):
        if texto == "dinheiro":
            print('dinheiro')
            self.tipo_pagamento.setText('DINHEIRO')
        elif texto == "pix":
            print('pix')
            self.tipo_pagamento.setText('PIX')
        elif texto == "cartao":
            print('cartao')
            self.tipo_pagamento.setText('CARTAO')
        elif texto == "nota": 
            self.tipo_pagamento.setText('NOTA')
            print('nota')
            self.abrir_janela_nota_venda()
        else:
            print('bunda')
            self.tipo_pagamento.setText('BUNDA') 

    def abrir_janela_nota_venda(self):
        self.janela_notas = abaNotasVendas()
        self.janela_notas.exec_()
        
    def fechar_compra(self):
        print('botao fechamento clicado !')
        with open('exemplo.txt', 'w') as arquivo:
            # Nada precisa ser escrito aqui, pois o arquivo já foi truncado
            pass
        self.salvar_notas_venda()
        self.pagina_principal.limpar_biblioteca()
        self.close()

    def conectar_carregar_compras(self):
        self.carregar_compras_do_arquivo()
        self.usuario_1.setText(self.nome_usuario)
        self.atualizar_interface()
        self.receber1.setText(f'{self.total_max.text()}')

        # Adicione a impressão da lista de compras no terminal
        for compra in self.lista_compras:
            print(compra)

    def carregar_compras_do_arquivo(self):
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                database="meubanco"
            )
            cursor = conexao.cursor()

            sql = "SELECT id FROM notas_vendas ORDER BY id DESC LIMIT 1"
            cursor.execute(sql)
            ultimo_registro = cursor.fetchone()
            if ultimo_registro:
                id_venda = ultimo_registro[0]
                self.ID_vendas.setText(str(id_venda))
            
            cursor.close()
            conexao.close()
        except mysql.connector.Error as erro:
            print('erro ao conectar-se ao banco de dados ', erro)

        lista_compras = []
        nome_arquivo = 'exemplo.txt'
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

        for linha in linhas:
            partes = linha.strip().split('|')
            partes = [parte.strip() for parte in partes]
            compra = {
                'nome_produto': partes[0],
                'quantidade': float(partes[1]),
                'preco_unitario': float(partes[2]),
                'subtotal': float(partes[3])
            }
            lista_compras.append(compra)

        self.lista_compras = lista_compras

    def atualizar_interface(self):
        self.total = sum(compra['subtotal'] for compra in self.lista_compras)

        valor_receber1 = float(self.receber1.text().replace('R$', '').replace(',', '') or 0)
        valor_receber2 = float(self.receber2.text().replace('R$', '').replace(',', '') or 0)
        desconto = 0

        valor_receber = self.total - valor_receber1 - valor_receber2

        self.labelTotal.setText(f'R${self.total:.2f}')
        self.labeDesconto.setText(f'R${desconto:.2f}')
        self.labeReceber.setText(f'R${valor_receber:.2f}')
        self.total_max.setText(f'{self.total:.2f}')
        self.receber_max.setText(f'R${valor_receber:.2f}')
        
    def salvar_notas_venda(self):
        print(self.nome_usuario)
        print(self.OBS.text())
        print(self.lista_compras)
        print(f'R${self.total:.2f}')
        print(self.tipo_pagamento.text())
        
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                database='meubanco'
            )
            cursor = conexao.cursor()

            sql = """INSERT INTO notas_vendas (usuario, lista_compra, total, forma_pagamento, OBS) 
                    VALUES (%s, %s, %s, %s, %s)"""
            valores = (self.nome_usuario, str(self.lista_compras), f'R${self.total:.2f}', self.tipo_pagamento.text(), self.OBS.text())
            cursor.execute(sql, valores)

            conexao.commit()
            cursor.close()
            conexao.close()

            print('Nota de venda salva com sucesso!')
        except mysql.connector.Error as erro:
            print('Erro ao conectar-se ao banco de dados:', erro)
         
class janelaproduto(QMainWindow):
    emitir_codigo = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        uic.loadUi("pesquisa_f8.ui", self)

        self.line_pesquisa = self.findChild(QLineEdit, "lineEdit")
        self.tabela = self.findChild(QTableWidget, "tableWidget")

        atalho_enter = QShortcut(QKeySequence(Qt.Key_Return),self)
        atalho_enter.activated.connect(self.ligar_enter_precionar)

        atalho_enter_num = QShortcut(QKeySequence(Qt.Key_Enter),self)
        atalho_enter_num.activated.connect(self.ligar_enter_precionar)

        self.ESC = QShortcut(QKeySequence(Qt.Key_Escape),self)
        self.ESC.activated.connect(self.fechar_janela)

        atalho_ceta = QShortcut(QKeySequence(Qt.Key_Down),self)
        atalho_ceta.activated.connect(self.move_focus)
        
    def fechar_janela(self):
        self.close()
        
    def ligar_enter_precionar(self):
        if self.line_pesquisa.hasFocus():
            self.procura_produto()
        elif self.tabela.hasFocus():
            self.seleciona_produto()

    def procura_produto(self):
        if self.line_pesquisa is not None:
            procura_text = self.line_pesquisa.text().strip()

            resultado = self.pesquisa_banco(procura_text)
            self.atualizar_tabela(resultado)
        else:
            print("NAO ENCONTRADO !!")
            
    def pesquisa_banco(self, procura_text):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            database='meubanco'
        )
        cursor = connection.cursor()
        comando = "SELECT nome, preco, codigo FROM produtos WHERE codigo = %s OR nome LIKE %s"
        cursor.execute(comando, (procura_text, '%' + procura_text + '%'))
        resultado = cursor.fetchall()
        connection.close()
        return resultado

    def atualizar_tabela(self, resultados):
        # Limpar a tabela antes de adicionar novos resultados
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)  # Defina o número correto de colunas

        # Adicionar resultados à tabela
        for row_num, row_data in enumerate(resultados):
            self.tableWidget.insertRow(row_num)

            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_num, col_num, item)

        # Definir largura da coluna (ajuste conforme necessário)
        for col_num in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(col_num, 300)

    
    
    def seleciona_produto(self):
        # Obtenha a linha selecionada
        selected_row = self.tableWidget.currentRow()

        # Certifique-se de que uma linha está selecionada
        if selected_row >= 0:
            # Obtenha os dados da linha selecionada
            nome = self.tableWidget.item(selected_row, 0).text()
            preco = self.tableWidget.item(selected_row, 1).text()
            codigo = int(self.tableWidget.item(selected_row, 2).text())
            # Exiba ou faça o que quiser com os dados
            print(f"Nome.janlea: {nome}, Preço: {preco}, Código: {codigo}")
            
            self.emitir_codigo.emit(codigo)
            self.close()
        else:
            print("Nenhuma linha selecionada.")

    def move_focus(self):
        if not self.tabela.hasFocus() and self.tabela.rowCount() > 0:
            self.tabela.setFocus()
            self.tabela.setCurrentCell(0 ,0)
            
            
            
            
            
class janelaNotas(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("notas.ui", self)
        self.ID = self.findChild(QLabel,"ID")
        self.pagamento = self.findChild(QLabel,"pagamento")
        self.pesquisa = self.findChild(QLineEdit,"pesquisa")
        self.datahora = self.findChild(QLabel,"datahora")
        self.obs = self.findChild(QLabel,"obs")
        self.total = self.findChild(QLabel,"total")
        self.ESC = QShortcut(QKeySequence(Qt.Key_Escape),self)
        self.ESC.activated.connect(self.fechar_janela)

        self.pesquisa.editingFinished.connect(self.pesquisa_no_banco)
        # Conectar o sinal de pressionamento de tecla do QLineEdit para realizar a pesquisa quando a tecla "Enter" for pressionada
        self.pesquisa.returnPressed.connect(self.pesquisa_no_banco)

    def pesquisa_no_banco(self):
        texto_pesquisa = self.pesquisa.text()
        if texto_pesquisa:
            try:
                id_pesquisa = int(texto_pesquisa)
                connection = mysql.connector.connect(
                host='localhost',
                user='root',
                database='meubanco'
                )
                curso = connection.cursor(dictionary=True)
                query = "SELECT * FROM notas_vendas WHERE ID = %s"
                curso.execute(query,(id_pesquisa,))

                nota = curso.fetchone()
                if nota:
                    self.ID.setText(str(nota["ID"]))
                    self.pagamento.setText(nota["forma_pagamento"])
                    self.total.setText(nota["total"])
                    self.obs.setText(nota["OBS"])
                    self.datahora.setText(str(nota["data_hora"]))
                else:
                    self.ID.clear()
                    self.pagamento.clear()
                    self.total.clear()
                    self.obs.clear()
                    self.datahora.clear()
                curso.close()
                connection.close()
            except mysql.connector.Error as error:
                print("erro ao connectar ao msql:",error)
        else:
            print("o campo de pesquisa esta vazio!!")
            


    def fechar_janela(self):
        self.close()


         
        
        
class JanelaProdutocomsulta(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("botao_f8.ui", self)
        
        # Adicione um widget de interface de usuário para pesquisa
        self.entrada_pesquisa = self.findChild(QLineEdit, "lineEdit")

        # Conecte a tecla Enter ao slot de pesquisa
        enter_atalho = QShortcut(QKeySequence(Qt.Key_Return), self)
        enter_atalho.activated.connect(self.procura_produto)
        self.ESC = QShortcut(QKeySequence(Qt.Key_Escape),self)
        self.ESC.activated.connect(self.fechar_janela)
        
    def fechar_janela(self):
        self.close()
            
    def procura_produto(self):
        # Obtenha o texto de pesquisa do campo de entrada
        procura_text = self.entrada_pesquisa.text().strip()

        # Realize a pesquisa no banco de dados
        results = self.perform_search(procura_text)

        # Exiba os resultados na interface do usuário
        self.display_results(results)

    def perform_search(self, procura_text):
        # Conecte ao banco de dados MySQL (substitua os parâmetros pelo seu banco de dados)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            database='meubanco'
        )
        cursor = connection.cursor()

        # Execute a consulta SQL para buscar produtos com base no código e nome
        query = "SELECT codigo, nome, preco FROM produtos WHERE codigo = %s OR nome LIKE %s"
        cursor.execute(query, (procura_text, '%' + procura_text + '%'))
        results = cursor.fetchall()

        # Feche a conexão com o banco de dados
        connection.close()

        return results

    def display_results(self, results):
        # Certifique-se de que há pelo menos um resultado antes de tentar acessá-lo
        print(results)
        if results:
            # Considere apenas o primeiro resultado (pode ajustar conforme necessário)
            primeiro_resultado = results[0]

            # Extrai as informações do primeiro resultado
            codigo, nome, preco = primeiro_resultado

            # Atualiza os QLabels na interface gráfica
            self.produto.setText(nome)
            self.preco.setText(str(preco))
            self.codigo.setText(str(codigo))
            
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    nome_usuario = "NomeDoUsuario" 
    window = janelaproduto()
    window.show()
    sys.exit(app.exec_())