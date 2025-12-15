from database.connection import db

class Carrinho(db.Model):
    __tablename__ = 'tb_item_carrinho'
    item_id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('tb_livro.livro_id'), nullable=False, unique=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Float, nullable=False)