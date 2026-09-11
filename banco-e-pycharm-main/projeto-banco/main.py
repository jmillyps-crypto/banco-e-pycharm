from flask import Flask, render_template, request, flash, redirect, url_for
import fdb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Aqui_e_a_chave_da_turma_a'

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCOO\BANCO.FDB'
user = 'sysdba'
password = 'sysdba'

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

if __name__ == '__main__':
    app.run(debug=True)