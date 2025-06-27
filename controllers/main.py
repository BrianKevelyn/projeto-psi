from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    return render_template('index.html', nome=current_user.usu_nome)

@main_bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', nome=current_user.usu_nome)
