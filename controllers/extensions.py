from flask_mail import Mail
from database.connection import db
from flask_login import LoginManager

mail = Mail()
login_manager = LoginManager()
