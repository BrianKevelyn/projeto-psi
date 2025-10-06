from database.connection import db

class Carrinho(db.Model):
    __tablename__ = 'tb_carrinho'
    car_id = db.Column(db.Integer, primary_key=True)
    
