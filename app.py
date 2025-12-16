from flask import Flask
from controllers.extensions import mail, login_manager, db
from controllers.auth import auth_bp
from controllers.main import main_bp
from controllers.livros import livros_bp
from controllers.car import carrinho_bp
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'prfvictor191@gmail.com'
    app.config['MAIL_PASSWORD'] = 'qfaxuoyljiiooyeo'
    app.config['MAIL_DEFAULT_SENDER'] = 'prfvictor191@gmail.com'
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(livros_bp)
    app.register_blueprint(carrinho_bp)

    with app.app_context():
        db.create_all()

    return app
