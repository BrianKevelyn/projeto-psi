from database.connection import db

class Livro(db.Model):
    __tablename__ = 'tb_livros'

    liv_id = db.Column(db.Integer, primary_key=True)
    liv_titulo = db.Column(db.String(200), nullable=False)
    liv_descricao = db.Column(db.String(450), nullable=False)
    liv_editora = db.Column(db.String(100))
    liv_ano = db.Column(db.Integer)
    liv_autor = db.Column(db.String(100))
    liv_genero = db.Column(db.String(50))
    liv_quantidade = db.Column(db.Integer)
    liv_preco = db.Column(db.Float, nullable=False, default=0.0)