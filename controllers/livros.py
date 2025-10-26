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

@livros_bp.route('/editar/<int:livro_id>', methods=['GET', 'POST'])
@login_required
def editar_livro(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    if current_user.usu_tipo != "bibliotecario":
        flash("Você não tem permissão para editar livros.", "danger")
        return redirect(url_for('livros.lista_livros'))

    if request.method == "POST":
        livro.liv_titulo = request.form['titulo']
        livro.liv_autor = request.form['autor']
        livro.liv_editora = request.form['editora']
        livro.liv_ano = request.form['ano']
        livro.liv_genero = request.form['genero']
        livro.liv_preco = request.form['preco']
        livro.liv_descricao = request.form['descricao']
        livro.liv_quantidade = request.form['quantidade']
        db.session.commit()

        flash("Livro atualizado com sucesso!", "success")
        return redirect(url_for('livros.lista_livros'))

    return render_template('editar_livro.html', livro=livro)

@livros_bp.route('/lista_livros')
@login_required
def lista_livros():
    livros = Livro.query.all()

    emprestimos_usuario = Emprestimo.query.filter_by(emp_usu_id=current_user.usu_id).all()
    meus_livros = [emp.livro for emp in emprestimos_usuario]

    return render_template('livros_lista.html', livros=livros, meus_livros=meus_livros)

@livros_bp.route('/comprar/<int:livro_id>', methods=['POST'])
@login_required
def comprar_livro(livro_id):
    livro = Livro.query.get_or_404(livro_id)

    if livro.liv_quantidade < 1:
        flash("Livro indisponível no momento.", "error")
        return redirect(url_for('livros.lista_livros'))

    hoje = datetime.now().date()
    devolucao = hoje + timedelta(days=7)  

    emprestimo = Emprestimo(
        emp_usu_id=current_user.usu_id,
        emp_liv_id=livro.liv_id,
        emp_data_emprestimo=hoje,
        emp_data_a_devolver=devolucao,
        status="Em andamento"
    )

    db.session.add(emprestimo)
    livro.liv_quantidade -= 1
    db.session.commit()

    flash(f"Você comprou/empréstimo do livro '{livro.liv_titulo}' foi registrado com sucesso!", "success")
    return redirect(url_for('livros.lista_livros'))

@livros_bp.route('/excluir_livro/<int:livro_id>', methods=['POST'])
@login_required
def excluir_livro(livro_id):
    if current_user.usu_tipo != 'bibliotecario':
        flash("Você não tem permissão para fazer isso.", "error")
        return redirect(url_for('livros.lista_livros'))

    livro = Livro.query.get_or_404(livro_id)

    # Verifica se há empréstimos ativos
    emprestimos_existentes = Emprestimo.query.filter_by(emp_liv_id=livro.liv_id, status="Em andamento").first()
    if emprestimos_existentes:
        flash(f"Não é possível excluir '{livro.liv_titulo}' porque existem empréstimos ativos.", "error")
        return redirect(url_for('livros.lista_livros'))

    db.session.delete(livro)
    db.session.commit()
    flash(f"Livro '{livro.liv_titulo}' excluído com sucesso!", "success")
    return redirect(url_for('livros.lista_livros'))



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
            emp_usu_id=current_user.usu_id, 
            emp_liv_id=livro.liv_id,
            emp_data_emprestimo=hoje,
            emp_data_a_devolver=devolucao,
            status="Em andamento"
        )
        db.session.add(emprestimo)
        livro.liv_quantidade -= 1
        db.session.commit()

        flash("Empréstimo registrado com sucesso!", "success")
        return redirect(url_for('livros.emprestimo_livro'))

    # pega livros disponíveis
    livros_disponiveis = Livro.query.filter(Livro.liv_quantidade > 0).all()

    # pega empréstimos do usuário
    if current_user.usu_tipo == 'bibliotecario':
        emprestimos = Emprestimo.query.all()
    else:
        emprestimos = Emprestimo.query.filter_by(emp_usu_id=current_user.usu_id).all()

    # 🔹 Atualiza status para "Atrasado" se a data de devolução já passou
    hoje = date.today()
    atualizou = False

    for emp in emprestimos:
        data_limite = emp.emp_data_a_devolver
        if isinstance(data_limite, datetime):
            data_limite = data_limite.date()

        if emp.status.lower() != "devolvido" and data_limite and data_limite < hoje:
            if emp.status.lower() != "atrasado":
                emp.status = "Atrasado"
                atualizou = True

    if atualizou:
        db.session.commit()

    # 🔹 O return deve ficar no final da função, fora do for e fora dos ifs
    return render_template(
        'emprestimo_livro.html',
        livros=livros_disponiveis,
        emprestimos=emprestimos
    )


@livros_bp.route('/emprestimo_livro/<int:liv_id>')
@login_required
def emprestimo_por_livro(liv_id):
    hoje = date.today()
    atualizou = False

    for emp in emprestimos:
        # garante que emp_data_a_devolver seja do tipo date
        data_limite = emp.emp_data_a_devolver
        if isinstance(data_limite, datetime):
            data_limite = data_limite.date()

        # verifica se já passou da data limite e não está devolvido
        if emp.status.lower() != "devolvido" and data_limite and data_limite < hoje:
            if emp.status.lower() != "atrasado":
                emp.status = "Atrasado"
                atualizou = True

        if atualizou:
            db.session.commit()

    return render_template('emprestimo_livro.html', livro=livro, emprestimos=emprestimos)



@livros_bp.route('/emprestimos')
@login_required
def listar_emprestimos():
    if current_user.usu_tipo == 'bibliotecario':
        emprestimos = Emprestimo.query.all()
    else:
        emprestimos = Emprestimo.query.filter_by(emp_usu_id=current_user.usu_id).all()

    hoje = date.today()
    atualizou = False

    for emp in emprestimos:
        # garante que emp_data_a_devolver seja do tipo date
        data_limite = emp.emp_data_a_devolver
        if isinstance(data_limite, datetime):
            data_limite = data_limite.date()

        # verifica se já passou da data limite e não está devolvido
        if emp.status.lower() != "devolvido" and data_limite and data_limite < hoje:
            if emp.status.lower() != "atrasado":
                emp.status = "Atrasado"
                atualizou = True

    if atualizou:
        db.session.commit()

    return render_template('listar_emprestimos.html', emprestimos=emprestimos)
