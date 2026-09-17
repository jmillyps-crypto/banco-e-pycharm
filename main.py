from flask import Flask, render_template, request, flash, redirect, url_for
import fdb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Aqui_e_a_chave_da_turma_a'

host = 'localhost'
database = r'C:\Users\marco\Downloads\banco-e-pycharm\BANCO.FDB'
user = 'SYSDBA'
password = 'SYSDBA'

con = fdb.connect(host=host, database=database, user=user, password=password)

@app.route('/')
def index():
    cursor = con.cursor() #abrindo o cursor

    cursor.execute("""SELECT l.id_livro,l.NOME, l.AUTOR, l.ANO_PUBLICACAO 
                            FROM LIVRO l 
                            order by l.nome """)

    livros = cursor.fetchall()

    cursor.close()
    return render_template('livros.html', livros=livros)

@app.route('/novo')
def novo():
    return render_template('novo.html')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['titulo']
    autor = request.form['autor']
    ano_publicacao = request.form['ano_publicacao']

    cursor = con.cursor()

    try:
        cursor.execute("""SELECT 1 FROM LIVRO l WHERE nome = ?""", (nome,))
        if cursor.fetchone():
            flash('Erro: Livro já cadastrado')
            return redirect(url_for('novo'))

        cursor.execute( """ INSERT INTO livro (nome,autor, ano_publicacao)
                            VALUES (?, ? ,?)""", (nome, autor, ano_publicacao))

        con.commit()
        flash("Livro cadastrado com sucesso")
        return redirect(url_for('index'))

    except Exception as e:
        flash(f"Ocorreu um error -> {e}")
        con.rollback()
        return redirect(url_for('novo'))

    finally:
        cursor.close()



@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    cursor = con.cursor()
    try:
        cursor.execute("""SELECT id_livro, nome, autor, ano_publicacao from livro WHERE ID_LIVRO = ?""", (id,))
        livro = cursor.fetchone()
        print(livro)

        if not livro:
            flash('Livro não encontrado')
            return redirect(url_for('index'))

        if request.method == 'POST':
            nome = request.form['titulo']
            autor = request.form['autor']
            ano_publicacao = request.form['ano_publicacao']

            cursor.execute(""" UPDATE LIVRO SET nome = ?, autor = ?, ano_publicacao = ?
                               where id_livro = ?""", (nome, autor, ano_publicacao, id))
            con.commit()
            flash("Livro editado com sucesso")
            return redirect(url_for('index'))

        return render_template('editar.html', livro=livro)

    except Exception as e:
            con.rollback()
            flash(f"Ocorreu um error -> {e}")
            return redirect(url_for('index'))


    finally:
        cursor.close()

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    cursor = con.cursor()
    try:
        cursor.execute("""DELETE FROM livro WHERE ID_LIVRO = ?""", (id,))
        con.commit()
        flash("Livro deletado com sucesso")
        return redirect(url_for('index'))

    except Exception as e:
        con.rollback()
        flash(f"Ocorreu um error -> {e}")
        return redirect(url_for('index'))
    finally:
        cursor.close()


@app.route('/lista_usu')
def lista_usu():
    cursor = con.cursor() #abrindo o cursor

    cursor.execute("""SELECT u.id_usuario,u.NOME, u.email, u.senha 
                            FROM usuario u
                            order by u.nome """)

    usuarios = cursor.fetchall()

    cursor.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/novo_usu')
def novo_usu():
    return render_template('novo_usuario.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    cursor = con.cursor()

    try:
        cursor.execute("""SELECT 1 FROM usuario u WHERE nome = ?""", (nome,))
        if cursor.fetchone():
            flash('Erro: Usuário já cadastrado')
            return redirect(url_for('novo_usu'))

        cursor.execute( """ INSERT INTO usuario (nome,email,senha)
                            VALUES (?, ? ,?)""", (nome, email, senha))

        con.commit()
        flash("Usuário cadastrado com sucesso")
        return redirect(url_for('lista_usu'))

    except Exception as e:
        flash(f"Ocorreu um error -> {e}")
        con.rollback()
        return redirect(url_for('novo_usu'))

    finally:
        cursor.close()


@app.route('/editar_usuario/<int:id>', methods=['GET','POST'])
def editar_usuario(id):
    cursor = con.cursor()
    try:
        cursor.execute("""SELECT id_usuario, nome, email, senha from usuario WHERE ID_usuario = ?""", (id,))
        usuario = cursor.fetchone()


        if not usuario:
            flash('Usuário não encontrado')
            return redirect(url_for('lista_usu'))

        if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            senha = request.form['senha']

            cursor.execute(""" UPDATE usuario SET nome = ?, email = ?, senha = ?
                               where id_usuario = ?""", (nome, email, senha, id))
            con.commit()
            flash("Usuário editado com sucesso")
            return redirect(url_for('lista_usu'))

        return render_template('editar_usuario.html', usuario=usuario)

    except Exception as e:
            con.rollback()
            flash(f"Ocorreu um error -> {e}")
            return redirect(url_for('lista_usu'))


    finally:
        cursor.close()

@app.route('/deletar_usuario/<int:id>', methods=['POST'])
def deletar_usuario(id):
    cursor = con.cursor()
    try:
        cursor.execute("""DELETE FROM usuario WHERE ID_usuario = ?""", (id,))
        con.commit()
        flash("Usuário deletado com sucesso")
        return redirect(url_for('lista_usu'))

    except Exception as e:
        con.rollback()
        flash(f"Ocorreu um error -> {e}")
        return redirect(url_for('lista_usu'))
    finally:
        cursor.close()



if __name__ == '__main__':
    app.run(debug=True)