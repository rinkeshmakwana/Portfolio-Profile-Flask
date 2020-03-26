from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = '9f90e6c07a001085a1c574e8df57b05e'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME='ricks14348@gmail.com',
    MAIL_PASSWORD='Ricky#acker',
)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/rinkesh_makwana'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from profile import routes
