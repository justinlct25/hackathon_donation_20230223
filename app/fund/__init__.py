from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '<insert your secret key here>'

# suppress SQLAlchemy warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'fund.db')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


from fund import routes
