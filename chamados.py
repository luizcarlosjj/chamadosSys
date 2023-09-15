from PyQt5 import uic,QtWidgets
import sqlite3

# Login Usuários
def login_task():
    nome_usuario = login.user.text()
    senha = login.passwd.text()
    tipo = login.combobox.currentText()
    tec = str('tecnico')
    clie = str('usuario')
    banco = sqlite3.connect("db/banco_chamados.db")
    cursor = banco.cursor()
    try:
        cursor.execute("SELECT senha FROM cadastros WHERE nome = '{}'" .format(nome_usuario))
        senha_bd = cursor.fetchall()
        cursor.execute("SELECT tipo FROM cadastros WHERE nome = '{}'" .format(nome_usuario))
        tipo_db = cursor.fetchall()
        banco.close()
    except:
        print('erro, usuario inválido.')

    if senha == senha_bd[0][0] and tipo_db[0][0] == tipo and tipo_db[0][0] == clie:
        tela_cliente.show()
        login.user.setText("")
        login.passwd.setText(" ")
        login.close()
        login.label_6.setText(" ")
    elif senha == senha_bd[0][0] and tipo_db[0][0] == tipo and tipo_db[0][0] == tec:
        tela_tecnico.show()
        login.user.setText("")
        login.passwd.setText(" ")
        login.close()
        login.label_6.setText(" ")
    else:
        login.label_6.setText("Dados de login incorretos")
# Cadastro Usuários
def cadastro_task():
    nome = tela_cadastro_user.user.text()
    senha = tela_cadastro_user.user_2.text()
    filial = tela_cadastro_user.filial.currentText()
    tipo = tela_cadastro_user.tipo.currentText()

    if (len(senha) > 0):
        try:
            banco = sqlite3.connect('db/banco_chamados.db')
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastros (nome text, filial text, tipo text, senha text)")
            cursor.execute("INSERT INTO cadastros VALUES ('"+nome+"','"+filial+"','"+tipo+"', '"+senha+"')")
            banco.commit()
            banco.close()
            tela_cadastro_user.label_3.setText("Usuário cadastrado com sucesso!")

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ", erro)
    else:
        tela_cadastro_user.label_3.setText("Digite uma senha válida!")
# Cadastro Chamados
def chamados_task():
    if tela_cadastro_chamados.radioButton.isChecked():
        opcao = ('Manutenção')
    elif tela_cadastro_chamados.radioButton_2.isChecked():
        opcao = ('Suporte')
    elif tela_cadastro_chamados.radioButton_3.isChecked():
        opcao = ('Dev')
    else: 
        opcao = ""

    status = str('Aberto')
    nome = tela_cadastro_chamados.lineEdit_2.text()
    descricao = tela_cadastro_chamados.lineEdit.text()
    categoria = str(opcao)

    banco = sqlite3.connect('db/banco_chamados.db')
    cursor = banco.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS chamados (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        nome_solicitante text, 
                        descricao VARCHAR(255), 
                        categoria text, 
                        status text);
                """)
    
    cursor.execute("INSERT INTO chamados (nome_solicitante, descricao, categoria, status) VALUES ('"+nome+"', '"+descricao+"', '"+categoria+"', '"+status+"')")
    banco.commit()
    banco.close()
    tela_cadastro_chamados.label_6.setText('Chamado Cadastrado!')
    tela_cadastro_chamados.lineEdit_2.setText('')
    tela_cadastro_chamados.lineEdit.setText('')
# Tratamento de Chamados
def tratar_task():
    tela_tratar_chamados.show()
    banco = sqlite3.connect('db/banco_chamados.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM chamados")
    dados_lidos = cursor.fetchall()

    tela_tratar_chamados.tableWidget.setRowCount(len(dados_lidos))
    tela_tratar_chamados.tableWidget.setColumnCount(5)
    tela_tratar_chamados.tableWidget.setHorizontalHeaderLabels(["id","Nome do Solicitante","Descição", "categoria", "Status"])

    rows = dados_lidos
    for i in range(len(rows)): #linha
        for j in range(len(rows[0])): #coluna
            item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
            tela_tratar_chamados.tableWidget.setItem(i,j, item)    
# Mostrar Estatisticas
def estatisticas_show():
    tela_estatisticas.show()
    sts_aberto = str('Aberto')
    sts_concluido = str('Concluido')
    sts_tratamento = str('Em tratamento')
    banco = sqlite3.connect("db/banco_chamados.db")
    cursor = banco.cursor()
    # Chamados em Aberto
    cursor.execute("SELECT * FROM chamados WHERE status = '{}'" .format(sts_aberto))
    result01 = str(len(cursor.fetchall()))
    # Chamados Concluidos
    cursor.execute("SELECT * FROM chamados WHERE status = '{}'" .format(sts_concluido))
    result02 = str(len(cursor.fetchall()))
    # Chamados em Tratamento
    cursor.execute("SELECT * FROM chamados WHERE status = '{}'" .format(sts_tratamento))
    result03 = str(len(cursor.fetchall()))
    # Labels:
    tela_estatisticas.label_4.setText(result01)
    tela_estatisticas.label_7.setText(result02)
    tela_estatisticas.label_5.setText(result03)

    banco.commit()
    banco.close()
# Selecionar Chamados
def selecionar_chamados():
    banco = sqlite3.connect("db/banco_chamados.db")
    cursor = banco.cursor()
    id_digitado = int(tela_selecionar_chamados.lineEdit.text())
    cursor.execute("UPDATE chamados SET status='Em tratamento' WHERE id={}".format(id_digitado))
    banco.commit()
    banco.close()
    tela_selecionar_chamados.label_2.setText('Atribuido com sucesso!')
    tela_selecionar_chamados.lineEdit.setText("")
# Concluir chamados
def alterar_status_chamados():
    banco = sqlite3.connect("db/banco_chamados.db")
    cursor = banco.cursor()
    id_digitado = int(tela_concluir_chamados.lineEdit.text())
    cursor.execute("UPDATE chamados SET status='Concluido' WHERE id={}".format(id_digitado))
    banco.commit()
    banco.close()
    tela_concluir_chamados.label_2.setText('Concluido com sucesso!')
    tela_concluir_chamados.lineEdit.setText("")
    

# abertura de telas:
def abrir_cadastro_user():
    login.close()
    tela_cadastro_user.show()
def abrir_cadastro_chamados():
    tela_cadastro_chamados.show()
def abrir_tratamento():
    tela_tratar_chamados.show()
def abrir_concluir_chamados():
    tela_concluir_chamados.show()
def abrir_selecionar_chamados():
    tela_selecionar_chamados.show()

# fechamento de telas:
def logout_cadastro_user():
    tela_cadastro_user.close()
    tela_cadastro_user.label_3.setText("")
    tela_cadastro_user.user.setText("")
    login.show()
def logout_tela_cliente():
    tela_cliente.close()
    login.show()
def logout_tela_tecnico():
    tela_tecnico.close()
    login.show()
def logout_tela_chamado():
    tela_cadastro_chamados.close()
    tela_cadastro_chamados.close()
def logout_chamados():
    tela_tratar_chamados.close()
def logout_estatisticas():
    tela_estatisticas.close()
def logout_concluir_chamados():
    tela_concluir_chamados.close()
    tela_tratar_chamados.show()
def logout_selecionar_chamados():
    tela_selecionar_chamados.close()
    tela_tratar_chamados.show()

app = QtWidgets.QApplication([])

# import Telas
login = uic.loadUi("pages/login.ui")
tela_cadastro_user = uic.loadUi("pages/cadastro.ui")
tela_cliente = uic.loadUi("pages/home_cliente.ui")
tela_tecnico = uic.loadUi("pages/home_tec.ui")
tela_cadastro_chamados = uic.loadUi("pages/cad_chamados.ui")
tela_tratar_chamados = uic.loadUi("pages/tratar_chamados.ui")
tela_estatisticas = uic.loadUi("pages/stats_chamados.ui")
tela_concluir_chamados = uic.loadUi("pages/concluir_chamados.ui")
tela_selecionar_chamados = uic.loadUi("pages/selecionar_chamados.ui")

# tela LOGIN
login.pushButton_2.clicked.connect(login_task)
login.pushButton_3.clicked.connect(abrir_cadastro_user)

# tela CADASTRO
tela_cadastro_user.filial.addItems(["","Lins 01","Lins 02"])
tela_cadastro_user.tipo.addItems(["","usuario","tecnico"])
tela_cadastro_user.pushButton_3.clicked.connect(cadastro_task)
tela_cadastro_user.pushButton_2.clicked.connect(logout_cadastro_user)

# tela CLIENTE
tela_cliente.pushButton.clicked.connect(abrir_cadastro_chamados)
tela_cliente.pushButton_3.clicked.connect(logout_tela_cliente)
tela_cliente.pushButton_4.clicked.connect(estatisticas_show)

# tela TECNICO
tela_tecnico.pushButton_2.clicked.connect(logout_tela_tecnico)
tela_tecnico.pushButton_3.clicked.connect(tratar_task)
tela_tecnico.pushButton_4.clicked.connect(estatisticas_show)

# tela CRIAR CHAMADOS
tela_cadastro_chamados.pushButton.clicked.connect(chamados_task)
tela_cadastro_chamados.comboBox.addItems(["","Lins 01","Lins 02"])
tela_cadastro_chamados.pushButton_2.clicked.connect(logout_tela_chamado)

# tela TRATAR CHAMADOS
tela_tratar_chamados.pushButton_2.clicked.connect(logout_chamados)
tela_tratar_chamados.pushButton_3.clicked.connect(abrir_concluir_chamados)
tela_tratar_chamados.pushButton_4.clicked.connect(abrir_selecionar_chamados)

# tela ESTATISTICAS
tela_estatisticas.pushButton_2.clicked.connect(logout_estatisticas)

# tela CONCLUIR CHAMADO
tela_concluir_chamados.pushButton.clicked.connect(alterar_status_chamados)
tela_concluir_chamados.pushButton_2.clicked.connect(logout_concluir_chamados)

# tela SELECIONAR CHAMADO
tela_selecionar_chamados.pushButton.clicked.connect(selecionar_chamados)
tela_selecionar_chamados.pushButton_2.clicked.connect(logout_selecionar_chamados)

login.show()
app.exec()