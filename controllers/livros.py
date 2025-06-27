from flask import Blueprint, render_template, request, redirect, url_for
from models.livro import Livro
from database.connection import db  # caso precise fazer commit

livros_bp = Blueprint('livros', __name__, url_prefix='/livros')

@livros_bp.route('/adicionar_livro', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        descricao = request.form.get('descricao')
        editora = request.form.get('editora')
        ano = request.form.get('ano')
        genero = request.form.get('genero')
        quantidade = request.form.get('quantidade')

        if titulo and autor:
            novo_livro = Livro(
                liv_titulo=titulo,
                liv_autor=autor,
                liv_descricao=descricao or '',
                liv_editora=editora or '',
                liv_ano=int(ano) if ano else None,
                liv_genero=genero or '',
                liv_quantidade=int(quantidade) if quantidade else 0
            )
            db.session.add(novo_livro)
            db.session.commit()
            return redirect(url_for('livros.lista_livros'))
        else:
            erro = "Por favor, preencha ao menos título e autor."
            return render_template('adicionar_livro.html', erro=erro)
    return render_template('adicionar_livro.html')


@livros_bp.route('/lista_livros')
def lista_livros():
    livros = Livro.query.all()  # busca todos os livros do banco
    return render_template('livros_lista.html', livros=livros)


@livros_bp.route('/emprestimo_livro')
def emprestimo_livro():
    return render_template('emprestimo_livro.html')
