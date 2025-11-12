from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app import db  # se seu app principal se chama app.py e possui db do SQLAlchemy

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    return render_template('index.html', nome=current_user.usu_nome)

@main_bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', nome=current_user.usu_nome)

@main_bp.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Atualiza os dados do usuário logado
        current_user.usu_nome = nome
        current_user.usu_telefone = telefone
        current_user.usu_email = email

        # Só atualiza a senha se o campo não estiver vazio
        if senha:
            current_user.usu_senha = generate_password_hash(senha)

        db.session.commit()

        return render_template('editar_perfil.html', mensagem="Perfil atualizado com sucesso!")

    return render_template('editar_perfil.html')
