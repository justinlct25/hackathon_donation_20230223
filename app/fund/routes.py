from fund import app, db
from flask import render_template, url_for, request, jsonify, redirect, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from fund.models import User
from fund.forms import RegistrationForm, LoginForm
import random

@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('index.html')

@app.route("/login", methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      print("successful login")
      flash('You\'ve successfully logged in,'+' '+ current_user.username +'!')
      return redirect(url_for('home'))
    flash('Invalid username or password.')
  return render_template('login.html',title='Login', form=form)

@app.route("/logout")
def logout():
  logout_user()
  flash('You\'re now logged out. Thanks for your visit!')
  return redirect(url_for('home'))

@app.route("/register", methods=['GET','POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    # form.validate_username(form.username.data)
    user = User(username=form.username.data, password=form.password.data, email=form.email.data, icon=f'default_{random.randint(0,9)}.png')
    db.session.add(user)
    db.session.commit()
    flash('Registration successful!')
    return redirect(url_for('registered'))
  return render_template('register.html',title='Register',form=form)

@app.route("/registered")
def registered():
  return render_template('registered.html', title='Thanks!')