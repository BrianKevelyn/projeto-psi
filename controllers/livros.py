from flask import Blueprint, render_template

livros_bp = Blueprint('livros', __name__, url_prefix='/livros')

@livros_bp.route('/')
def lista():
    # Aqui você buscaria os livros no banco e passaria para o template
    livros = [
        {'titulo': 'Livro A', 'autor': 'Autor A'},
        {'titulo': 'Livro B', 'autor': 'Autor B'},
    ]
    return render_template('livros_lista.html', livros=livros)
