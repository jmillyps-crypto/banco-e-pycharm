from flask import Flask, render_template, request, flash, redirect, url_for
import fdb

app = Flask(__name__)

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCOO\BANCO.FDB'
user = 'sysdba'
password = 'sysdba'

co = fdb.connect(host=host, database=database, user=user, password=password)

@app.route('/')
def index():
    cursor = co.cursor() #abrindo o cursor

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
    nome = request.form['nome']
    autor = request.form['autor']
    ano_publicacao = request.form['ano_publicacao']

    cursor = con.cursor()

    try:
        cursor.execute("""SELECT 1 FROM LIVRO l WHERE nome = ?""", (nome,))
        if cursor.fetchone():
            flash('Erro: Livro já cadastrado')
            return redirect(url_for('novo'))
    except Exception as e:

    finally:

if __name__ == '__main__':
    app.run(debug=True)
