import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
 
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
db = SQLAlchemy(app)
 
 
## MODELO TABELA ##
# 5 campos  #
 
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    NomeLivro = db.Column(db.Text)
    AutorLivro = db.Column(db.Text)
    DataPublicacao = db.Column(db.Text)
    QuantidadeLivro = db.Column(db.Integer)
 
    #setters
    def __init__(self, NomeLivro, AutorLivro, DataPublicacao, QuantidadeLivro):
 
        self.NomeLivro = NomeLivro
        self.AutorLivro = AutorLivro
        self.DataPublicacao = DataPublicacao
        self.QuantidadeLivro = QuantidadeLivro
 
 
@app.route('/')
def index():
    db.create_all()
    livros = Livro.query.all()
    return render_template('index.html', livros = livros)
 
 
#Create
@app.route('/inserir', methods=['POST'])
def insert():
    NomeLivro = request.form['nome']
    AutorLivro = request.form['autor']
    DataPublicacao = request.form['data']
    QuantidadeLivro = request.form['quantidade']
    livro = Livro(NomeLivro, AutorLivro, DataPublicacao, QuantidadeLivro)
    db.session.add(livro)
    db.session.commit()
    return redirect(url_for('index'))
 
#Read
@app.route('/listar_todos', methods=['POST'])
def listar():
    livros = Livro.query.all()
    return render_template('listartodos.html', livros = livros)
 
@app.route('/listar', methods=['POST'])
def list():
    id = request.form['id']
    livros = Livro.query.filter(Livro.id.like(f'%{id}%')).all()
    return render_template("listarid.html", livros = livros)

#Update.
@app.route('/atualizar/<int:id>', methods=['GET','POST'])
def update(id):
 
    if request.method == 'POST':
        novo_NomeLivro = request.form['novo_nome']
        novo_AutorLivro = request.form['novo_autor']
        nova_DataPublicacao = request.form['nova_data']
        nova_QuantidadeLivro = request.form['nova_quantidade']
        livro = Livro.query.get(id)
        livro.NomeLivro = novo_NomeLivro
        livro.AutorLivro = novo_AutorLivro
        livro.DataPublicacao = nova_DataPublicacao
        livro.QuantidadeLivro = nova_QuantidadeLivro
        db.session.commit()
        return redirect(url_for("index"))
    else:
        livro = Livro.query.get(id)
        return render_template('atualizar.html', livro = livro)

#Delete
@app.route('/excluir/<int:id>')
def delete(id):

    livro = Livro.query.get(id)
    db.session.delete(livro)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)