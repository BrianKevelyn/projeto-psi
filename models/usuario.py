from database.connection import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__ = 'tb_usuarios'

    usu_id = db.Column(db.Integer, primary_key=True)
    usu_nome = db.Column(db.String(100), nullable=False)
    usu_matricula = db.Column(db.String(50), unique=True, nullable=False)
    usu_telefone = db.Column(db.String(20))
    usu_email = db.Column(db.String(100), unique=True)
    usu_tipo = db.Column(db.String(50))
    usu_senha = db.Column(db.String(255), nullable=False)

    def set_senha(self, senha):
        self.usu_senha = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.usu_senha, senha)

    def get_id(self):
        return str(self.usu_id)
