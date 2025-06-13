from database.connection import db

class Emprestimo(db.Model):
    __tablename__ = 'tb_emprestimos'

    emp_id = db.Column(db.Integer, primary_key=True)
    emp_usu_id = db.Column(db.Integer, db.ForeignKey('tb_usuarios.usu_id'), nullable=False)
    emp_liv_id = db.Column(db.Integer, db.ForeignKey('tb_livros.liv_id'), nullable=False)
    emp_data_emprestimo = db.Column(db.Date)
    emp_data_a_devolver = db.Column(db.Date)
    emp_data_devolucao = db.Column(db.Date)
    status = db.Column(db.String(50))
