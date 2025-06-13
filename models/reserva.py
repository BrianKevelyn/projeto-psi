from database.connection import db

class Reserva(db.Model):
    __tablename__ = 'tb_reservas'

    res_id = db.Column(db.Integer, primary_key=True)
    res_usu_id = db.Column(db.Integer, db.ForeignKey('tb_usuarios.usu_id'), nullable=False)
    res_liv_id = db.Column(db.Integer, db.ForeignKey('tb_livros.liv_id'), nullable=False)
    res_data_reserva = db.Column(db.Date)
    status = db.Column(db.String(50))
