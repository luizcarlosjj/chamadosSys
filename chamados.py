from PyQt5 import uic,QtWidgets
import sqlite3

# Login Usuários
def showLogin():
    home.frame_Login.show()
    home.frame_Cadastro.close()
    home.frame_off_login.close()
def login_task():
    nome_usuario = home.user.text()
    senha = home.passwd.text()
    tipo = home.tipoLog.currentText()
    tec = str('tecnico')
    user = str('usuario')
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

    if senha == senha_bd[0][0] and tipo_db[0][0] == tipo: #and tipo_db[0][0] == user
        inicio.show()
        home.user.setText("")
        home.passwd.setText("")
        home.close()
        home.label_6.setText("")
    else:
        home.label_6.setText("Dados de login incorretos")
    '''elif senha == senha_bd[0][0] and tipo_db[0][0] == tipo and tipo_db[0][0] == tec:
        inicio.show()
        home.user.setText("")
        home.passwd.setText("")
        home.close()
        home.label_6.setText("")'''


    
    return tipo_db

# Cadastro Usuários
def showCadastro():
    home.frame_Cadastro.show()
    home.frame_Login.close()
    home.frame_off_login.close()
    home.resCad.setText("")
def cadastro_task():
    nome = home.nameCad.text()
    senha = home.senhaCad.text()
    tipo = home.tipoCad.currentText()
    filial = home.filialCad.currentText()

    if (len(senha) > 0):
        try:
            banco = sqlite3.connect('db/banco_chamados.db')
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastros (nome text, filial text, tipo text, senha text)")
            cursor.execute("INSERT INTO cadastros VALUES ('"+nome+"','"+filial+"','"+tipo+"', '"+senha+"')")
            banco.commit()
            banco.close()
            home.resCad.setText("Usuário cadastrado com sucesso! \n Realize Login")
            home.nameCad.setText("")
            home.senhaCad.setText("")
            home.repSenhaCad.setText("")
            itemInicial = ""
            home.filialCad.setCurrentText(itemInicial)
            home.tipoCad.setCurrentText(itemInicial)


        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ", erro)
    else:
        home.resCad.setText("Digite uma senha válida!")


# INICIO
def login_CadChamados():
    chamados.show()
    inicio.label_3.setText("")
def login_TratChamados():
    tipo = home.tipoLog.currentText()
    if tipo == 'usuario':
        inicio.label_3.setText('Usuário sem permissão para está ação!')
    elif tipo == 'tecnico':
        tela_tratar_chamados.show()
        inicio.close()
def logout_inicio():
    inicio.close()
    home.show()
    item = ""
    home.tipoLog.setCurrentText(item)
    home.label_6.setText("")
    inicio.label_3.setText("")

    home.frame_off_login.show()
    home.frame_Login.close()
    home.frame_Cadastro.close()


# CADASTRO DE CHAMADOS:
def chamados_task():
    if chamados.radioButton.isChecked():
        opcao = ('Manutenção')
    elif chamados.radioButton_2.isChecked():
        opcao = ('Suporte')
    elif chamados.radioButton_3.isChecked():
        opcao = ('Dev')
    else: 
        opcao = ""

    status = str('Aberto')
    nome = chamados.nameCmd.text()
    descricao = chamados.descCmd.text()
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
    cursor.execute("SELECT id FROM chamados WHERE nome_solicitante='{}'".format(nome))
    id_solicitante = cursor.fetchall()
    banco.commit()
    banco.close()
    chamados.label_6.setText('Chamado Cadastrado! o seu id é {}'.format(id_solicitante))
    chamados.nameCmd.setText('')
    chamados.descCmd.setText('')
    chamados.filialAtd.setCurrentText("")
def logout_chamados():
    chamados.close()


# TRATAMENTO DE CHAMADOS:
def chamados_View_Select(): # MOSTRAR TABELA DE DADOS SELECT
    tela_tratar_chamados.res_Conclui.setText("")# APAGAR TEXTO DA OUTRA TELA
    tela_tratar_chamados.res_Conclui_True.setText("")# APAGAR TEXTO DA OUTRA TELA
    tela_tratar_chamados.id_Conclui.setText("")# APAGAR ID DA OUTRA TELA

    tela_tratar_chamados.frame_select.show() # ABRIR FRAME SELECT
    tela_tratar_chamados.frame_conclui.close()# FECHAR FRAME CONCLUIR
    tela_tratar_chamados.frame_off.close()# FECHAR FRAME OFF
    tela_tratar_chamados.frame_search.close()

    banco = sqlite3.connect('db/banco_chamados.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM chamados")
    dados_lidos = cursor.fetchall()

    tela_tratar_chamados.tableWidgetSelect.setRowCount(len(dados_lidos))
    tela_tratar_chamados.tableWidgetSelect.setColumnCount(5)
    tela_tratar_chamados.tableWidgetSelect.setHorizontalHeaderLabels(["id","Nome do Solicitante","Descição", "categoria", "Status"])

    rows = dados_lidos
    for i in range(len(rows)): #linha
        for j in range(len(rows[0])): #coluna
            item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
            tela_tratar_chamados.tableWidgetSelect.setItem(i,j, item) 

def chamados_View_Concluir(): # MOSTRAR TABELA DE DADOS CONCLUIR

    tela_tratar_chamados.res_Select.setText("")
    tela_tratar_chamados.res_Select_True.setText("")
    tela_tratar_chamados.id_Select.setText("")

    tela_tratar_chamados.frame_conclui.show()
    tela_tratar_chamados.frame_select.close()
    tela_tratar_chamados.frame_off.close()

    banco = sqlite3.connect('db/banco_chamados.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM chamados")
    dados_lidos = cursor.fetchall()

    tela_tratar_chamados.tableWidgetConcluir.setRowCount(len(dados_lidos))
    tela_tratar_chamados.tableWidgetConcluir.setColumnCount(5)
    tela_tratar_chamados.tableWidgetConcluir.setHorizontalHeaderLabels(["id","Nome do Solicitante","Descição", "categoria", "Status"])

    rows = dados_lidos
    for i in range(len(rows)): #linha
        for j in range(len(rows[0])): #coluna
            item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
            tela_tratar_chamados.tableWidgetConcluir.setItem(i,j, item) 

def voltar():
    tela_tratar_chamados.close()
    inicio.show()
def limpar():
    tela_tratar_chamados.frame_conclui.close()
    tela_tratar_chamados.frame_select.close()
    tela_tratar_chamados.frame_off.show()
    
    tela_tratar_chamados.res_Select.setText("")
    tela_tratar_chamados.res_Select_True.setText("")
    tela_tratar_chamados.id_Select.setText("")

    tela_tratar_chamados.res_Conclui.setText("")
    tela_tratar_chamados.res_Conclui_True.setText("")
    tela_tratar_chamados.id_Conclui.setText("")

def selecionar_chamados(): ##  EM ABERTO --> EM TRATAMENTO
    banco = sqlite3.connect("db/banco_chamados.db")
    cursor = banco.cursor()
    id_digitado = int(tela_tratar_chamados.id_Select.text())
    cursor.execute("SELECT status FROM chamados WHERE id='{}'".format(id_digitado))
    status_id = cursor.fetchall() 
    if status_id[0][0] == 'Em tratamento':    
        tela_tratar_chamados.res_Select.setText("Chamado Já está em Tratamento!")  
    elif status_id[0][0] == 'Concluido':
        tela_tratar_chamados.res_Select.setText("Chamado Já está Concluído!")
    elif status_id[0][0] == "Aberto": # SE ESSE FOR VERDADE IRÁ REALIZAR
        tela_tratar_chamados.res_Select_True.setText('Atribuido com sucesso!')
        tela_tratar_chamados.res_Select.setText("")
        tela_tratar_chamados.id_Select.setText("")
        cursor.execute("UPDATE chamados SET status='Em tratamento' WHERE id={}".format(id_digitado))
        banco.commit()
        banco.close()        
        
        chamados_View_Select()
    else:
        print('error')

def concluir_chamados(): ##  EM TRATAMENTO --> CONCLUIDO
    banco = sqlite3.connect("db/banco_chamados.db")
    cursor = banco.cursor()
    id_digitado = int(tela_tratar_chamados.id_Conclui.text())
    cursor.execute("SELECT status FROM chamados WHERE id='{}'".format(id_digitado))
    status_id = cursor.fetchall() 
    if status_id[0][0] == 'Concluido':
        tela_tratar_chamados.res_Conclui.setText("Chamado já está Concluído!")
    elif status_id[0][0] == 'Em tratamento':
        tela_tratar_chamados.res_Conclui_True.setText("Concluído com Sucesso!")
        tela_tratar_chamados.res_Conclui.setText("")

        tela_tratar_chamados.id_Conclui.setText("")
        cursor.execute("UPDATE chamados SET status='Concluido' WHERE id={}".format(id_digitado))
        banco.commit()
        banco.close()
        chamados_View_Concluir()
    else:
        print('error')

def buscarChamados():
    tela_tratar_chamados.frame_search.show()
    tela_tratar_chamados.frame_conclui.close()
    tela_tratar_chamados.frame_select.close()
    tela_tratar_chamados.frame_off.close()

    banco = sqlite3.connect("db/banco_chamados.db")
    cursor = banco.cursor()
    id_buscar = int(tela_tratar_chamados.idSearch.text())
    cursor.execute("SELECT * FROM chamados WHERE id='{}'".format(id_buscar))
    id_encontrado = cursor.fetchall()
    tela_tratar_chamados.tableWidgetBuscar.setRowCount(len(id_encontrado))
    tela_tratar_chamados.tableWidgetBuscar.setColumnCount(5)
    tela_tratar_chamados.tableWidgetBuscar.setHorizontalHeaderLabels(["id","Nome do Solicitante","Descição", "categoria", "Status"])

    rows = id_encontrado
    for i in range(len(rows)): #linha
        for j in range(len(rows[0])): #coluna
            item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
            tela_tratar_chamados.tableWidgetBuscar.setItem(i,j, item) 

def concluir_chamados_buscado():
    banco = sqlite3.connect("db/banco_chamados.db")
    cursor = banco.cursor()
    id_buscado = int(tela_tratar_chamados.idSearch.text())
    cursor.execute("SELECT status FROM chamados WHERE id='{}'".format(id_buscado))
    status_id = cursor.fetchall() 
    if status_id[0][0] == 'Concluido':
        tela_tratar_chamados.res_ConcluirBuscar.setText("Chamado já está Concluído!")
    elif status_id[0][0] == 'Em tratamento':
        tela_tratar_chamados.res_ConcluirBuscar_True.setText("Concluído com Sucesso!")
        tela_tratar_chamados.res_ConcluirBuscar.setText("")
        tela_tratar_chamados.idSearch.setText("")
        cursor.execute("UPDATE chamados SET status='Concluido' WHERE id={}".format(id_buscado))
        banco.commit()
        banco.close()
        buscarChamados()
    else:
        print('error')

def selecionar_chamados_buscados(): ##  EM ABERTO --> EM TRATAMENTO
    banco = sqlite3.connect("db/banco_chamados.db")
    cursor = banco.cursor()
    id_digitado = int(tela_tratar_chamados.idSearch.text())
    cursor.execute("SELECT status FROM chamados WHERE id='{}'".format(id_digitado))
    status_id = cursor.fetchall() 
    if status_id[0][0] == 'Em tratamento':    
        tela_tratar_chamados.res_SelectBuscar.setText("Chamado Já está em Tratamento!")  
    elif status_id[0][0] == 'Concluido':
        tela_tratar_chamados.res_SelectBuscar.setText("Chamado Já está Concluído!")
    elif status_id[0][0] == "Aberto": # SE ESSE FOR VERDADE IRÁ REALIZAR
        tela_tratar_chamados.res_SelectBuscar_True.setText('Atribuido com sucesso!')
        tela_tratar_chamados.res_SelectBuscar.setText("")
        tela_tratar_chamados.idSearch.setText("")
        cursor.execute("UPDATE chamados SET status='Em tratamento' WHERE id={}".format(id_digitado))
        banco.commit()
        banco.close()        
        
        buscarChamados()
    else:
        print('error')

# Mostrar Estatisticas
def estatisticas_show():
    estatisticas.show()
    inicio.label_3.setText("")
    sts_aberto = str('Aberto')
    sts_concluido = str('Concluido')
    sts_tratamento = str('Em tratamento')
    banco = sqlite3.connect("db/banco_chamados.db")
    cursor = banco.cursor()
    # Chamados em Aberto
    cursor.execute("SELECT * FROM chamados WHERE status = '{}'" .format(sts_aberto))
    resultAberto = str(len(cursor.fetchall()))
    # Chamados Concluidos
    cursor.execute("SELECT * FROM chamados WHERE status = '{}'" .format(sts_concluido))
    resultConcluido = str(len(cursor.fetchall()))
    # Chamados em Tratamento
    cursor.execute("SELECT * FROM chamados WHERE status = '{}'" .format(sts_tratamento))
    resultTratados = str(len(cursor.fetchall()))
    # Labels:
    estatisticas.resAberto.setText(resultAberto)
    estatisticas.resConcluidos.setText(resultConcluido)
    estatisticas.resTrat.setText(resultTratados)

    banco.commit()
    banco.close()
def logout_estatisticas():
    estatisticas.close()


app = QtWidgets.QApplication([])
# import Telas
home = uic.loadUi("pages/login.ui")
inicio = uic.loadUi("pages/inicio.ui")
chamados = uic.loadUi("pages/chamadosCad.ui")
tela_tratar_chamados = uic.loadUi("pages/tratar_chamados.ui")
estatisticas = uic.loadUi("pages/estatisticas.ui")

# tela HOME
home.frame_off_login.show()
home.btn_Login.clicked.connect(showLogin) # MOSTRA ABA DE LOGIN
home.btn_Entrar.clicked.connect(login_task) # EXECUTA LOGIN
home.btn_Cadastro.clicked.connect(showCadastro) # MOSTRA ABA DE CADASTRO
home.btn_Cad.clicked.connect(cadastro_task) # EXECUTA CADASTRO
home.tipoCad.addItems(["","usuario","tecnico"]) # ADICIONA DADOS AO COMBO BOX "TIPO"
home.filialCad.addItems(["","Lins 01","Lins 02"]) # ADICIONA DADOS AO COMBO BOX "FILIAL"

# tela INICIO
inicio.btnCadCmd.clicked.connect(login_CadChamados)
inicio.btnTratCmd.clicked.connect(login_TratChamados)
inicio.btnStats.clicked.connect(estatisticas_show)
inicio.btnSairHome.clicked.connect(logout_inicio)

# tela CADASTAR CHAMADOS
chamados.btnCadCmd.clicked.connect(chamados_task)
chamados.btnSairCadCmd.clicked.connect(logout_chamados)
chamados.filialAtd.addItems(["","Lins 01","Lins 02"])

# tela TRATAR CHAMADOS
tela_tratar_chamados.frame_off.show()
tela_tratar_chamados.btn_Select.clicked.connect(chamados_View_Select) # MOSTRAR ABA SELECIONAR CHAMADOS
tela_tratar_chamados.btn_Concluir.clicked.connect(chamados_View_Concluir) # MOSTRAR ABA CONCLUIR CHAMADOS
tela_tratar_chamados.btn_Limpar.clicked.connect(limpar) # LIMPAR TELA
tela_tratar_chamados.btn_Voltar.clicked.connect(voltar) # VOLTAR

tela_tratar_chamados.btn_SelectCmd.clicked.connect(selecionar_chamados) # EXECUTAR SELECT CHAMADOS
tela_tratar_chamados.btn_ConcluirCmd.clicked.connect(concluir_chamados) # EXECUTAR CONCLUIR CHAMADOS

tela_tratar_chamados.btn_Buscar.clicked.connect(buscarChamados)
tela_tratar_chamados.btn_ConcluirCmd_2.clicked.connect(concluir_chamados_buscado)
tela_tratar_chamados.btn_SelectCmd_2.clicked.connect(selecionar_chamados_buscados) 

# tela ESTATISTICAS
estatisticas.btnVoltarStats.clicked.connect(logout_estatisticas)

home.show()
app.exec()