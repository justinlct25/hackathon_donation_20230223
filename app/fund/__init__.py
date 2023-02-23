from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '<insert your secret key here>'

# suppress SQLAlchemy warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


basedir = os.path.abspath(os.path.dirname(__file__))

# DB Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c22011528:Twente0508$@csmysql.cs.cf.ac.uk:3306/c22011528_donation'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'fund.db')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from fund import models
from fund import routes
