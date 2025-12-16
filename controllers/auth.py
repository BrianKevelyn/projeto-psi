from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models.usuario import Usuario
from database.connection import db
from flask_mail import Message

auth_bp = Blueprint('auth', __name__)

def enviar_email_login(usuario):
    msg = Message(
        subject='Novo login detectado',
        recipients=[usuario.usu_email],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )

    msg.body = f"""Olá, {usuario.usu_nome}!

Detectamos um novo login em sua conta.

Se não foi você, entre em contato com o suporte imediatamente.
"""

    mail = current_app.extensions['mail']
    mail.send(msg)




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        matricula = request.form.get('matricula', '').strip()
        senha = request.form.get('senha', '')

        usuario = Usuario.query.filter_by(usu_matricula=matricula).first()
        if usuario and usuario.check_senha(senha):
            login_user(usuario)
            enviar_email_login(usuario)
            flash('Login realizado com sucesso!', 'success')  # Mensagem de sucesso no login
            return redirect(url_for('main.index'))
        else:
            flash('Usuário ou senha inválidos', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        matricula = request.form.get('matricula', '').strip()
        telefone = request.form.get('telefone', '').strip()
        email = request.form.get('email', '').strip().lower()
        tipo = request.form.get('tipo', '').strip().lower()
        senha = request.form.get('senha', '')

        if Usuario.query.filter_by(usu_matricula=matricula).first():
            flash('Matrícula já cadastrada.', 'warning')
            return redirect(url_for('auth.register'))

        if Usuario.query.filter_by(usu_email=email).first():
            flash('Email já cadastrado.', 'warning')
            return redirect(url_for('auth.register'))

       
        novo_usuario = Usuario(
            usu_nome=nome,
            usu_matricula=matricula,
            usu_telefone=telefone,
            usu_email=email,
            usu_tipo=tipo
        )
        novo_usuario.set_senha(senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Usuário criado com sucesso. Faça login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

