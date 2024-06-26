from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from datetime import datetime

import os
import psycopg2 #pip install psycopg2  
import psycopg2.extras

CREATE_ENDERECO_TABLE = (
    "CREATE TABLE IF NOT EXISTS endereco (id SERIAL PRIMARY KEY, rua TEXT, cep TEXT, cidade TEXT, bairro TEXT, pais TEXT);"
)


CREATE_PESSOA_TABLE = (
    "CREATE TABLE IF NOT EXISTS pessoa(id SERIAL PRIMARY KEY, endereco_id integer, nome TEXT, sobrenome TEXT, email TEXT, telefone TEXT, data_nasc DATE, genero TEXT, FOREIGN KEY (endereco_id) REFERENCES endereco(id));"
)

CREATE_FACILITADORES_TABLE = (
    "CREATE TABLE IF NOT EXISTS facilitadores (id SERIAL PRIMARY KEY, pessoa_id integer, area TEXT, horario CHARACTER VARYING, localizacao CHARACTER VARYING, data_contrato DATE, salario TEXT, FOREIGN KEY (pessoa_id) REFERENCES pessoa(id));"
)

CREATE_ESTUDANTES_TABLE = (
    "CREATE TABLE IF NOT EXISTS estudantes (id SERIAL PRIMARY KEY, pessoa_id integer, data_matricula DATE, numero_matricula INTEGER, status smallint NOT NULL, FOREIGN KEY (pessoa_id)  REFERENCES pessoa(id));"
)
CREATE_CURSOS_TABLE = (
    "CREATE TABLE IF NOT EXISTS Cursos (id SERIAL PRIMARY KEY, nome_curso TEXT, descricao TEXT, duracao TEXT, modulos TEXT);"
)
CREATE_TURMAS_TABLE = (
    "CREATE TABLE IF NOT EXISTS Turmas (id SERIAL PRIMARY KEY, Cursos_id integer, Facilitadores_id integer, nome_turma TEXT, horario TEXT, localizacao TEXT, data_inicio DATE, data_termino DATE, FOREIGN KEY (Cursos_id)  REFERENCES Cursos(id), FOREIGN KEY (Facilitadores_id)  REFERENCES Facilitadores(id));"
)

load_dotenv()
url = os.getenv("DATABASE_URL")

app = Flask(__name__)
app.secret_key="fpzivhzm"
#configurações do banco de dados
try:
    db_connection = psycopg2.connect(url)
    cursor = db_connection.cursor()
    cursor.execute(CREATE_ENDERECO_TABLE)
    cursor.execute(CREATE_PESSOA_TABLE)
    cursor.execute(CREATE_ESTUDANTES_TABLE)
    cursor.execute(CREATE_FACILITADORES_TABLE)
    cursor.execute(CREATE_CURSOS_TABLE)
    cursor.execute(CREATE_TURMAS_TABLE)

except psycopg2.Error as e:
    print("Erro ao conectar ao banco de dados:", e)

# DB_HOST = "localhost"
# DB_NAME = "resiliadata"
# DB_USER = "postgres"
# DB_PASS = "ravula32"

# conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password = DB_PASS, host=DB_HOST)

########### ROTA HOME ###########################
@app.route('/')
def home():
    

    return render_template('home.html')

###########CURSO#######################
@app.route('/exibirFacilitadores')
def exibirFacilitadores():
    try:
        # Criar uma nova conexão e cursor usando o padrão de gerenciamento de contexto 'with'
        with psycopg2.connect(url) as db_connection:
            with db_connection.cursor() as cursor:
                sql = "SELECT * FROM facilitadores"
                cursor.execute(sql)
                lista_facilitadores = cursor.fetchall()
                return render_template('facilitadores/facilitadores.html', lista_facilitadores=lista_facilitadores)
    except psycopg2.Error as e:
        flash("Erro ao executar a consulta no banco de dados")
        print("Erro ao executar a consulta:", e)
        return redirect(url_for('home'))

    
@app.route('/add_facilitadores', methods=['POST'])
def add_facilitadores():
    try:
        if request.method == 'POST':
            # Dados do formulário
            nome = request.form['nome']
            sobrenome = request.form['sobrenome']
            email = request.form['email']
            telefone = request.form['telefone']
            
            # Formatar a data de nascimento para o formato correto (aaaa-mm-dd)
            data_nasc = datetime.strptime(request.form['data_nasc'], '%d/%m/%Y').strftime('%Y-%m-%d')
            
            genero = request.form['genero']
            area = request.form['area']
            horario = request.form['horario']
            localizacao = request.form['localizacao']
            
            # Formatar a data de contrato para o formato correto (aaaa-mm-dd)
            data_contrato = datetime.strptime(request.form['data_contrato'], '%d/%m/%Y').strftime('%Y-%m-%d')
            
            salario = request.form['salario']
            rua = request.form['rua']
            cep = request.form['cep']
            cidade = request.form['cidade']
            bairro = request.form['bairro']
            pais = request.form['pais']

            # Criar uma nova conexão e cursor usando o padrão de gerenciamento de contexto 'with'
            with psycopg2.connect(url) as db_connection:
                with db_connection.cursor() as cursor:
                    # Inserir dados de endereço
                    cursor.execute("INSERT INTO Endereco (rua, cep, cidade, bairro, pais) VALUES (%s,%s,%s,%s,%s) RETURNING id", (rua, cep, cidade, bairro, pais))
                    endereco_id = cursor.fetchone()[0]  # Obtém o ID do endereço inserido
                    
                    # Inserir dados de pessoa associando o ID do endereço
                    cursor.execute("INSERT INTO Pessoa (endereco_id, nome, sobrenome, email, telefone, data_nasc, genero) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id", (endereco_id, nome, sobrenome, email, telefone, data_nasc, genero))
                    pessoa_id = cursor.fetchone()[0] # Obtém o ID da pessoa inserida

                    # Inserir dados do facilitador associando o ID da pessoa
                    cursor.execute("INSERT INTO Facilitadores (pessoa_id, area, horario, localizacao, data_contrato, salario) VALUES (%s, %s, %s, %s, %s, %s)", (pessoa_id, area, horario, localizacao, data_contrato, salario))

            flash('Facilitador cadastrado com sucesso!')
            return redirect(url_for('exibirFacilitadores'))
    except psycopg2.Error as e:
        flash("Erro ao cadastrar facilitador")
        print("Erro ao cadastrar facilitador:", e)
        return redirect(url_for('home'))
    
@app.route('/updateFacilitadores/<id>', methods=['POST'])
def updateFacilitadores(id):
    if request.method == 'POST':
        area = request.form['area']
        horario = request.form['horario']
        localizacao = request.form['localizacao']
        # Formatar a data de contrato para o formato correto (aaaa-mm-dd)
        data_contrato = datetime.strptime(request.form['data_contrato'], '%d/%m/%Y').strftime('%Y-%m-%d')
        salario = request.form['salario']

        try:
            # Criar uma nova conexão e cursor usando o padrão de gerenciamento de contexto 'with'
            with psycopg2.connect(url) as db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE Facilitadores
                        SET area = %s,
                            horario = %s,
                            localizacao = %s,
                            data_contrato = %s,
                            salario = %s
                        WHERE id = %s
                    """, (area, horario, localizacao, data_contrato, salario, id))
                    flash('Facilitador foi atualizado com sucesso!')
                    db_connection.commit()
                    return redirect(url_for('exibirFacilitadores'))
        except psycopg2.Error as e:
            flash("Erro ao atualizar o facilitador no banco de dados")
            print("Erro ao atualizar o facilitador:", e)
            return redirect(url_for('exibirEstudantes'))

    
@app.route('/editFacilitadores/<id>', methods=['POST', 'GET'])
def editFacilitadores(id):
    try:
        # Criar uma nova conexão e cursor usando o padrão de gerenciamento de contexto 'with'
        with psycopg2.connect(url) as db_connection:
            with db_connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Facilitadores WHERE id = %s', (id,))
                data = cursor.fetchall()
                return render_template('facilitadores/editFacilitadores.html', facilitadores=data[0])
    except psycopg2.Error as e:
        flash("Erro ao editar facilitador")
        print("Erro ao editar facilitador:", e)
        return redirect(url_for('home'))

@app.route('/deleteFacilitadores/<string:id>', methods=['POST', 'GET'])
def deleteFacilitadores(id):
    try:
        # Criação da conexão com o banco de dados
        with psycopg2.connect(url) as db_connection:
            # Criação do cursor dentro do contexto da conexão
            with db_connection.cursor() as cursor:

                # Seleciona o id da pessoa associada ao facilitador
                cursor.execute('SELECT pessoa_id FROM Facilitadores WHERE id = {0}'.format(id))
                pessoa_id = cursor.fetchone()[0]
                print(f"Pessoa ID: {pessoa_id}")
                

                # Seleciona o id do endereço associado à pessoa
                cursor.execute('SELECT endereco_id FROM Pessoa WHERE id = {0}'.format(pessoa_id))
                endereco_id = cursor.fetchone()[0]

                print(f"Endereço ID: {endereco_id}")

                # Deleta o registro da tabela facilitadores
                cursor.execute('DELETE FROM Facilitadores WHERE id = {0}'.format(id))
                
                            
                # Deleta o registro da tabela pessoa associado ao facilitador
                cursor.execute('DELETE FROM Pessoa WHERE id = %s',(pessoa_id,))
                
                              
                # Deleta o registro da tabela endereco associado à 
                # pessoa
                cursor.execute('DELETE FROM Endereco WHERE id = %s',(endereco_id,))
                
                # Commit das alterações no banco de dados
                db_connection.commit()

        # Redireciona para a página de exibição de facilitadores após a exclusão
        flash('Funcionário deletado com sucesso!')
        return redirect(url_for('exibirFacilitadores'))

    except psycopg2.Error as e:
        # Tratamento de exceção para erros no psycopg2
        # Isso pode incluir logging do erro, retornar uma mensagem de erro personalizada para o cliente, etc.
        print("Erro ao acessar o banco de dados:", e)
        # Retorna uma resposta HTTP 500 - Erro interno do servidor
        return "Ocorreu um erro interno do servidor.", 500

###########FACILITADOR################
#############TURMA###################
@app.route('/exibirTurmas')
def exibirTurmas():
    sql = "SELECT * from Turmas"
    cursor.execute(sql)
    lista_turmas = cursor.fetchall()
    return render_template('turmas/turmas.html', lista_turmas = lista_turmas)

@app.route('/addTurmas', methods = ['POST'] )
def addTurmas():
    if request.method == 'POST':
        # Dados do formulário
        nome_turma = request.form['nome_turma']
        horario = request.form['horario']
        localizacao = request.form['localizacao']
        data_inicio = request.form['data_inicio']
        data_termino = request.form['data_termino']
        # Inserir dados de pessoa associando o ID do endereço
        cursor.execute("INSERT INTO Turmas ( nome_turma, horario, localizacao, data_inicio, data_termino) VALUES (%s,%s,%s,%s, %s) RETURNING id", (nome_turma, horario, localizacao, data_inicio, data_termino))
        Cursos_id = cursor.fetchone()[0] # Obtém o ID do endereço inserido
        db_connection.commit()
        flash('Estudante cadastrado com sucesso!')
        return redirect(url_for('exibirTurmas'))
    
@app.route('/updateTurmas/<id>', methods=['POST'])
def updateTurmas(id):
    if request.method == 'POST':
        nome_turma = request.form['nome_turma']
        horario = request.form['horario']
        localizacao = request.form['localizacao']
        data_inicio = request.form['data_inicio']
        data_termino = request.form['data_termino']
        
                
        cursor.execute("""
        UPDATE Turmas
        SET nome_turma = %s,
            horario = %s,
            localizacao = %s,
            data_inicio = %s,
            data_termino = %s
            
        WHERE id = %s
        """, (nome_turma, horario, localizacao, data_inicio,data_termino, id))
        flash('Turma foi atualizado com sucesso!')
        db_connection.commit()
        return redirect(url_for('exibirTurmas'))
        
@app.route('/editTurmas/<id>', methods = ['POST', 'GET'])
def editTurmas(id):
    cursor.execute('Select * FROM Turmas WHERE id = {0}'.format(id))
    data = cursor.fetchall()
    
    return render_template('turmas/editTurmas.html', turmas = data[0] )

@app.route('/deleteTurmas/<string:id>', methods = ['POST','GET'])
def deleteTurmas(id):
    cursor.execute(
        'DELETE FROM Cursos Where id = {0}'.format(id)
    )
    cursor.execute(
        'DELETE FROM Turmas Where id = {0}'.format(id)
    )
   
    db_connection.commit()
    flash('Turma Deletada!')
    return redirect(url_for('exibirTurmas'))
#############TURMA###################

###############CURSOS#####################
@app.route('/exibirCursos')
def exibirCursos():
    try:
        with psycopg2.connect(url) as db_connect:
            with db_connect.cursor() as cursor:
                sql = "SELECT * from Cursos"
                cursor.execute(sql)
                lista_cursos = cursor.fetchall()
                return render_template('cursos/cursos.html', lista_cursos = lista_cursos)
    except psycopg2.Error as e:  
        # Tratamento de exceção para erros no psycopg2
        # Isso pode incluir logging do erro, retornar uma mensagem de erro personalizada para o cliente, etc.
        print("Erro ao acessar o banco de dados:", e)
        # Retorna uma resposta HTTP 500 - Erro interno do servidor
        return "Ocorreu um erro interno do servidor.", 500
    

@app.route('/addCursos', methods = ['POST'] )
def addCursos():
    try:
        if request.method == 'POST':
            # Dados do formulário
            nome_curso = request.form['nome_curso']
            descricao = request.form['descricao']
            duracao = request.form['duracao']
            modulos = request.form['modulos']
        with psycopg2.connect(url) as db_connect:
            with db_connect.cursor() as cursor:
                # Inserir dados de pessoa associando o ID do endereço
                cursor.execute("INSERT INTO Cursos( nome_curso, descricao, duracao, modulos) VALUES (%s,%s,%s,%s) RETURNING id", (nome_curso, descricao, duracao, modulos))
                #Pessoa_id = cursor.fetchone()[0] # Obtém o ID do endereço inserido
                db_connection.commit()
                flash('Curso cadastrado com sucesso!')
                return redirect(url_for('exibirCursos'))
    except psycopg2.Error as e:
        # Tratamento de exceção para erros no psycopg2
        # Isso pode incluir logging do erro, retornar uma mensagem de erro personalizada para o cliente, etc.
        print("Erro ao acessar o banco de dados:", e)
        # Retorna uma resposta HTTP 500 - Erro interno do servidor
        return "Ocorreu um erro interno do servidor.", 500
    
        
    
@app.route('/updateCursos/<id>', methods=['POST'])
def updateCursos(id):
    if request.method == 'POST':
        nome_curso = request.form['nome_curso']
        descricao = request.form['descricao']
        duracao = request.form['duracao']
        modulos = request.form['modulos']
        try:
            with psycopg2.connect(url) as db_connect:
                with db_connect.cursor() as cursor:
                     cursor.execute("""
                    UPDATE Cursos
                    SET nome_curso = %s,
                        descricao = %s,
                        duracao = %s,
                        modulos = %s
                        
                    WHERE id = %s
                    """, (nome_curso, descricao, duracao, modulos, id))
                flash('Curso foi atualizado com sucesso!')
                db_connection.commit()
                return redirect(url_for('exibirCursos'))
        except psycopg2.Error as e:
            # Tratamento de exceção para erros no psycopg2
            # Isso pode incluir logging do erro, retornar uma mensagem de erro personalizada para o cliente, etc.
            print("Erro ao acessar o banco de dados:", e)
            # Retorna uma resposta HTTP 500 - Erro interno do servidor
            return "Ocorreu um erro interno do servidor.", 500
       
        
@app.route('/editCursos/<id>', methods = ['POST', 'GET'])
def editCursos(id):
    try:
        with psycopg2.connect(url) as db_connection:
            with db_connection.cursor() as cursor:
                cursor.execute('Select * FROM Cursos WHERE id = {0}'.format(id))
                data = cursor.fetchall()
                return render_template('cursos/editCursos.html', cursos = data[0] )
    except psycopg2.Error as e:
        # Tratamento de exceção para erros no psycopg2
        # Isso pode incluir logging do erro, retornar uma mensagem de erro personalizada para o cliente, etc.
        print("Erro ao acessar o banco de dados:", e)
        # Retorna uma resposta HTTP 500 - Erro interno do servidor
        return "Ocorreu um erro interno do servidor.", 500

@app.route('/deleteCursos/<string:id>', methods = ['POST','GET'])
def deleteCursos(id):
    try:
        with psycopg2.connect(url) as db_connection:
            with db_connection.cursor() as cursor:
                cursor.execute(
                'DELETE FROM Cursos Where id = {0}'.format(id))
    
                db_connection.commit()
                flash('Curso Deletado!')
                return redirect(url_for('exibirCursos'))
    except psycopg2.Error as e:
        # Tratamento de exceção para erros no psycopg2
        # Isso pode incluir logging do erro, retornar uma mensagem de erro personalizada para o cliente, etc.
        print("Erro ao acessar o banco de dados:", e)
        # Retorna uma resposta HTTP 500 - Erro interno do servidor
        return "Ocorreu um erro interno do servidor.", 500

    
  

###########ESTUDANTE###################
### cADASTRAR ESTUDANTE ###

@app.route('/add_estudante', methods=['POST'])
def add_estudante():
    try:
        if request.method == 'POST':
            # Dados do formulário
            nome = request.form['nome']
            sobrenome = request.form['sobrenome']
            email = request.form['email']
            telefone = request.form['telefone']
            
            # Formatar a data de nascimento para o formato correto (aaaa-mm-dd)
            data_nasc = datetime.strptime(request.form['data_nasc'], '%d/%m/%Y').strftime('%Y-%m-%d')
            
            genero = request.form['genero']
            
            # Formatar a data de matrícula para o formato correto (aaaa-mm-dd)
            data_matricula = datetime.strptime(request.form['data_matricula'], '%d/%m/%Y').strftime('%Y-%m-%d')
            
            numero_matricula = request.form['numero_matricula']
            status = request.form['status']
            rua = request.form['rua']
            cep = request.form['cep']
            cidade = request.form['cidade']
            bairro = request.form['bairro']
            pais = request.form['pais']

        with psycopg2.connect(url) as db_connection:
            with db_connection.cursor() as cursor:
                # Inserir dados de endereço
                cursor.execute("INSERT INTO Endereco (rua, cep, cidade, bairro, pais) VALUES (%s,%s,%s,%s,%s) RETURNING id", (rua, cep, cidade, bairro, pais))
                endereco_id = cursor.fetchone()[0]  # Obtém o ID do endereço inserido
                
                # Inserir dados de pessoa associando o ID do endereço
                cursor.execute("INSERT INTO Pessoa (endereco_id, nome, sobrenome, email, telefone, data_nasc, genero) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id", (endereco_id, nome, sobrenome, email, telefone, data_nasc, genero))
                pessoa_id = cursor.fetchone()[0] # Obtém o ID da pessoa inserida

                # Inserir dados do estudante associando o ID da pessoa
                cursor.execute("INSERT INTO Estudantes (pessoa_id, data_matricula, numero_matricula, status) VALUES (%s, %s, %s, %s)", (pessoa_id, data_matricula, numero_matricula, status))

                db_connection.commit()

                flash('Estudante cadastrado com sucesso!')
                return redirect(url_for('exibirEstudantes'))
    

    except psycopg2.Error as e:
        flash("Erro ao cadastrar Estudante")
        print("Erro ao cadastrar Estudante:", e)
        return redirect(url_for('home'))
    
        
        
        
### EXIBIR OS VALORES ESTUDANTES ###    

@app.route('/exibirEstudantes')
def exibirEstudantes():
    try:
        with psycopg2.connect(url) as db_connection:
            with db_connection.cursor() as cursor:
                sql = "SELECT * FROM Estudantes"
                cursor.execute(sql)
                lista_estudantes = cursor.fetchall()
                return render_template('estudante.html', lista_estudantes = lista_estudantes)
    except psycopg2.Error as e:
        flash("Erro ao executar a consulta no banco de dados")
        print("Erro ao executar a consulta:", e)
        return redirect(url_for('home'))
### EDIT ESTUDANTE ###

@app.route('/editEstudante/<id>', methods = ['POST', 'GET'])
def editEstudante(id):
    try:
        with psycopg2.connect(url) as db_connection:
            with db_connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Estudantes WHERE id = {0}'.format(id))
                data = cursor.fetchall()
                print(data[0])
    
                return render_template('editEstudante.html', estudante = data[0])
    except:
        flash("Erro ao editar facilitador")
        print("Erro ao editar facilitador:", e)
        return redirect(url_for('home'))
    
    

### ATUALIZAR OS DADOS  ###

@app.route('/updateEstudante/<id>', methods=['POST'])
def updateEstudante(id):
    if request.method == 'POST': 
         # Formatar a data de matrícula para o formato correto (aaaa-mm-dd)
        data_matricula = datetime.strptime(request.form['data_matricula'], '%d/%m/%Y').strftime('%Y-%m-%d')
        numero_matricula = request.form['numero_matricula']
        status = request.form['status']
        
        try:
            with psycopg2.connect(url) as db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute(cursor.execute("""
                    UPDATE Estudantes
                    SET data_matricula = %s,
                        numero_matricula=%s,
                        status = %s
                    
                    WHERE id = %s
                    """, (data_matricula,numero_matricula, status, id)))
        except:
            flash('Estudante foi atualizado com sucesso!')
            db_connection.commit()
            return redirect(url_for('exibirEstudantes'))
        
       
        
### DELETAR DADOS ###
@app.route('/deleteEstudantes/<string:id>', methods=['POST', 'GET'])
def deleteEstudantes(id):
    try:
        # Criação da conexão com o banco de dados
        with psycopg2.connect(url) as db_connection:
            # Criação do cursor dentro do contexto da conexão
            with db_connection.cursor() as cursor:
                # Seleciona o id da pessoa associada ao estudante
                cursor.execute('SELECT pessoa_id FROM Estudantes WHERE id = {0}'.format(id))
                pessoa_id = cursor.fetchone()[0]
                print(f"Pessoa ID deletado: {pessoa_id}")

                # Seleciona o id do endereço associado à pessoa
                cursor.execute('SELECT endereco_id FROM Pessoa WHERE id = {0}'.format(pessoa_id))
                endereco_id = cursor.fetchone()[0]
                print(f"Endereço ID deletado: {endereco_id}")

                # Deleta o registro da tabela estudantes
                cursor.execute('DELETE FROM Estudantes WHERE id = {0}'.format(id))

                # Deleta o registro da tabela pessoa associado ao estudante
                cursor.execute('DELETE FROM Pessoa WHERE id = %s', (pessoa_id,))

                # Deleta o registro da tabela endereco associado à pessoa
                cursor.execute('DELETE FROM Endereco WHERE id = %s', (endereco_id,))

                # Commit das alterações no banco de dados
                db_connection.commit()
                flash('Estudante Deletado')
                return redirect(url_for('exibirEstudantes'))
    except psycopg2.Error as e:
        # Tratamento de exceção para erros no psycopg2
        # Isso pode incluir logging do erro, retornar uma mensagem de erro personalizada para o cliente, etc.
        print("Erro ao acessar o banco de dados:", e)
        # Retorna uma resposta HTTP 500 - Erro interno do servidor
        return "Ocorreu um erro interno do servidor.", 500

########### ROTA PESSOA #########################


### MOSTRAR DADOS NA TELA ###
@app.route('/exibirPessoa')
def Index():
    
    sql = "SELECT * FROM Pessoa"
    cursor.execute(sql) #Executar a query do SQL
    lista_pessoa = cursor.fetchall()
    
    return render_template('pessoa.html', lista_pessoa = lista_pessoa)

######  INSERIR DADOS #######

@app.route('/add_pessoa', methods=['POST'])
def add_pessoa():

    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nasc = request.form['data_nasc']
        genero = request.form['genero']

        cursor.execute("INSERT INTO Pessoa (nome, sobrenome,email, telefone, data_nasc,genero) VALUES (%s,%s,%s,%s,%s,%s)", (nome, sobrenome, email,telefone,data_nasc,genero))
        db_connection.commit()
        flash('Pessoa cadastrada com sucesso!')
        return redirect(url_for('Index'))
    
### EDITAR DADOS ###

@app.route('/edit/<id>', methods = ['POST', 'GET'])

def get_pessoa(id):
    cursor.execute('SELECT * FROM Pessoa WHERE id = %s', (id))
    data = cursor.fetchall()
    print(data[0])
    return render_template('editPessoa.html', pessoa = data[0])

### ATUALIZAR OS DADOS  ###

@app.route('/update/<id>', methods=['POST'])
def update_pessoa(id):
    if request.method == 'POST': 
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nasc = request.form['data_nasc']
        genero = request.form['genero']

        cursor.execute("""
        UPDATE Pessoa
        SET nome = %s,
            sobrenome=%s,
            email = %s,
            telefone = %s,
            data_nasc = %s,
            genero = %s
        WHERE id = %s
        """, (nome,sobrenome,email,telefone,data_nasc,genero,id))
        flash('Pessoa foi atualiza com sucesso!')
        db_connection.commit()
        return redirect(url_for('exibirPessoa'))
        
### DELETE ###

@app.route('/delete/<string:id>', methods = ['POST', 'GET'])
def delete_student(id):
    
    cursor.execute(
        'DELETE FROM Pessoa Where id = {0}'.format(id)
    
    )
    db_connection.commit()
    flash('Pessoa Deletada')
    return redirect(url_for('exibirPessoa'))

if __name__ == "__main__":
    app.run(debug=True)