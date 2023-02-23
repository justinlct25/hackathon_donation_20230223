from datetime import datetime
from fund import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)



@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))