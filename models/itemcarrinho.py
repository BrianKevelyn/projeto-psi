from database.connection import db

class ItemCarrinho(db.Model):
    __tablename__ = 'item_carrinho'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('tb_usuarios.usu_id'), nullable=False)

    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario