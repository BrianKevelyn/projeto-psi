from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.livro import Livro
from models.emprestimo import Emprestimo
from database.connection import db
from datetime import datetime, date, timedelta

livros_bp = Blueprint('livros', __name__, url_prefix='/livros')

@livros_bp.route('/adicionar_livro', methods=['GET', 'POST'])
@login_required
def adicionar_livro():
    if current_user.usu_tipo != 'bibliotecario':
        flash("Você não tem permissão para acessar esta página.", "error")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        descricao = request.form.get('descricao')
        editora = request.form.get('editora')
        ano = request.form.get('ano')
        genero = request.form.get('genero')
        quantidade = request.form.get('quantidade')
        preco = request.form.get('preco')

        if not titulo or not autor:
            flash("Por favor, preencha ao menos título e autor.", "error")
            return render_template('adicionar_livro.html',
                                   titulo=titulo,
                                   autor=autor,
                                   descricao=descricao,
                                   editora=editora,
                                   ano=ano,
                                   genero=genero,
                                   quantidade=quantidade,
                                   preco=preco)

        try:
            ano_int = int(ano) if ano else None
        except ValueError:
            flash("Ano inválido.", "error")
            ano_int = None

        try:
            quantidade_int = int(quantidade) if quantidade else 0
        except ValueError:
            flash("Quantidade inválida.", "error")
            quantidade_int = 0

        try:
            preco_float = float(preco) if preco else None
        except ValueError:
            flash("Preço inválido.", "error")
            preco_float = None

        novo_livro = Livro(
            liv_titulo=titulo,
            liv_autor=autor,
            liv_descricao=descricao or '',
            liv_editora=editora or '',
            liv_ano=ano_int,
            liv_genero=genero or '',
            liv_quantidade=quantidade_int,
            liv_preco=preco_float
        )
        db.session.add(novo_livro)
        db.session.commit()
        flash("Livro adicionado com sucesso!", "success")
        return redirect(url_for('livros.lista_livros'))

    return render_template('adicionar_livro.html')

@livros_bp.route('/lista_livros')
@login_required
def lista_livros():
    livros = Livro.query.all()
    return render_template('livros_lista.html', livros=livros)

@livros_bp.route('/detalhes/<int:livro_id>')
@login_required
def detalhes_livro(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    return render_template('livros_detalhes.html', livro=livro)

@livros_bp.route('/emprestimo_livro', methods=['GET', 'POST'])
@login_required
def emprestimo_livro():
    if request.method == 'POST':
        livro_id = request.form.get('livro_id')
        livro = Livro.query.get(livro_id)
        if not livro:
            flash("Livro não encontrado.", "error")
            return redirect(url_for('livros.emprestimo_livro'))
        
        if livro.liv_quantidade < 1:
            flash("Livro indisponível para empréstimo.", "error")
            return redirect(url_for('livros.emprestimo_livro'))

        hoje = datetime.now().date()
        devolucao = hoje + timedelta(days=7)
        
        emprestimo = Emprestimo(
            emp_usu_id=current_user.id,
            emp_liv_id=livro.liv_id,
            emp_data_emprestimo=hoje,
            emp_data_a_devolver=devolucao,
            status="Em andamento"
        )
        db.session.add(emprestimo)
        livro.liv_quantidade -= 1
        db.session.commit()

        flash("Empréstimo registrado com sucesso!", "success")
        return redirect(url_for('main.index'))

    livros_disponiveis = Livro.query.filter(Livro.liv_quantidade > 0).all()
    return render_template('emprestimo_livro.html', livros=livros_disponiveis)

@livros_bp.route('/emprestimos')
@login_required
def listar_emprestimos():
    if current_user.usu_tipo == 'bibliotecario':
        emprestimos = Emprestimo.query.all()
    else:
        emprestimos = Emprestimo.query.filter_by(emp_usu_id=current_user.usu_id).all()

    return render_template('listar_emprestimos.html', emprestimos=emprestimos)
