from fund import app, db
from flask import render_template, url_for, request, jsonify, redirect, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from fund.models import User, Project, ProjectGoal, DonationPeriod, DonationAmount, DonationPlan, DonationRecord, ProjectComment
from fund.forms import RegistrationForm, LoginForm, AddProjectForm, AddGoalForm, ProjectCommentForm
import random

@app.route('/')
@app.route('/home')
def home():
    projects = Project.query.all()
    print(current_user)
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        return render_template('index.html', user=user, projects=projects)
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
  return render_template('login_blue.html',title='Login', form=form)

@app.route("/logout")
def logout():
  logout_user()
  flash('You\'re now logged out. Thanks for your visit!')
  return redirect(url_for('home'))

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, email=form.email.data, icon=f'default_{random.randint(0,9)}.png')
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('registered'))
    return render_template('register.html',title='Register',form=form)

@app.route("/registered")
def registered():
  return render_template('registered.html', title='Thanks!')

@app.route("/campaign")
def campaign():
  return render_template('campaign.html', title='Campaign')

@app.route("/addproject", methods=['GET', 'POST'])
def addProject():
    form = AddProjectForm()
    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.descripiton.data, service_target=form.service_target.data, funding_target=form.funding_target.data, before_date=form.before_date.data)
        project.managers.append(user)
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
    periods = DonationPeriod.query.all()
    amounts = DonationAmount.query.all()
    is_manager = True if user in project.managers else False
    comment_form = ProjectCommentForm()
    return render_template('project.html', user=user, is_manager=is_manager, project=project, periods=periods, amounts=amounts, comment_form=comment_form)

@app.route("/addgoal/<int:prj_id>", methods=['GET', 'POST'])
@login_required
def addGoal(prj_id):
    form = AddGoalForm()
    user = User.query.get(current_user.id)
    project = Project.query.get_or_404(prj_id)
    if form.validate_on_submit():
        goal = ProjectGoal(name=form.name.data, funding_required=form.funding_required.data, project_id=prj_id)
        project = Project.query.get(prj_id)
        db.session.add(goal)
        db.session.flush()
        db.session.refresh(goal)
        project.goals.append(goal)
        db.session.commit()
        flash("Goal added")
        return redirect(url_for('project', prj_id=project.id))
    return render_template('addgoal.html', user=user, project=project, form=form)

@app.route("/donation/<int:prj_id>", methods=['GET', 'POST'])
def addDonation(prj_id):
    json = request.json
    amount = DonationAmount.query.get_or_404(json['amount_id'])
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        project = Project.query.get(prj_id)
        project.donaters.append(user)
        user_id = current_user.id
    else:
        user_id = 0
    record = DonationRecord(donater_id=user_id, project_id=prj_id, amount=amount.amount)
    db.session.add(record)
    db.session.flush()
    db.session.refresh(record)
    user.donated_amount = int(user.donated_amount or 0) + amount.amount
    user.donate_record.append(record)
    if current_user.is_authenticated and json['is_period']:
        period = DonationPeriod.query.get_or_404(json['period_id'])
        plan = DonationPlan(donater_id=user_id)
        plan.amount.append(amount)
        plan.period.append(period)
        plan.records.append(record)
        db.session.add(plan)
    db.session.commit()
    return redirect(url_for('project', prj_id=prj_id))

@app.route("/comment/<int:prj_id>", methods=['POST'])
@login_required
def comment(prj_id):
    form = ProjectCommentForm()
    comment = ProjectComment(comment=form.comment.data, project_id=prj_id, user_id=current_user.id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("project", prj_id=prj_id))

@app.route("/profile/<int:user_id>", methods=["GET"])
def profile(user_id):
    if current_user.is_authenticated:
        is_owner = user_id == current_user.id
    else:
        is_owner = False   
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', is_owner=is_owner, user=user)
