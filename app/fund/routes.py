from fund import app, db
from flask import render_template, url_for, request, jsonify, redirect, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from fund.models import User, Project
from fund.forms import RegistrationForm, LoginForm, AddProjectForm
import random

@app.route('/')
@app.route('/home')
def home():
    # user = User.query.get(current_user.id)
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

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
  return render_template('login.html',title='Login', form=form, user=user)

@app.route("/logout")
def logout():
  logout_user()
  flash('You\'re now logged out. Thanks for your visit!')
  return redirect(url_for('home'))

@app.route("/register", methods=['GET','POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    form.validate_username(form.username.data)
    user = User(username=form.username.data, password=form.password.data, email=form.email.data, icon=f'default_{random.randint(0,9)}.png')
    db.session.add(user)
    db.session.commit()
    flash('Registration successful!')
    return redirect(url_for('registered'))
  return render_template('register.html',title='Register',form=form)

@app.route("/registered")
def registered():
  return render_template('registered.html', title='Thanks!')

@app.route("/addproject", methods=['GET', 'POST'])
def addProject():
    form = AddProjectForm()
    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.descripiton.data, service_target=form.service_target.data, funding_target=form.funding_target.data, before_date=form.before_date.data)
        project.prj_managers.append(user)
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!')
        return redirect(url_for('home'))
    return render_template('addproject.html', title="Add Project", form=form, user=user)

@app.route("/project/<int:prj_id>")
@login_required
def project(prj_id):
    user= User.query.get(current_user.id)
    project = Project.query.get_or_404(prj_id)
    print(project.managers)
    return render_template('project.html', user=user, project=project)