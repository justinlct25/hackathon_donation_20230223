from datetime import datetime
from fund import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

project_manager_association_table = db.Table('project_manager',
                                            db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
                                            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                            db.PrimaryKeyConstraint('project_id', 'user_id')
                                            )

project_donator_association_table = db.Table('project_donator',
                                            db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
                                            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                            db.PrimaryKeyConstraint('project_id', 'user_id')
                                            )

project_tag_association_table = db.Table('project_tag',
                                        db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
                                        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                                        db.PrimaryKeyConstraint('project_id', 'tag_id')
                                        )

user_donation_plan_association_table = db.Table('user_donation_plan',
                                                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                                db.Column('donation_plan_id', db.Integer, db.ForeignKey('donation_plan.id')),
                                                db.PrimaryKeyConstraint('user_id', 'donation_plan_id')
                                                )

plan_amount_association_table = db.Table('plan_amount', 
                                            db.Column('plan_id', db.Integer, db.ForeignKey('donation_plan.id')),
                                            db.Column('amount_id', db.Integer, db.ForeignKey('donation_amount.id')),
                                            db.PrimaryKeyConstraint('plan_id', 'amount_id')
                                        )

plan_period_association_table = db.Table('plan_period', 
                                            db.Column('plan_id', db.Integer, db.ForeignKey('donation_plan.id')),
                                            db.Column('period_id', db.Integer, db.ForeignKey('donation_period.id')),
                                            db.PrimaryKeyConstraint('plan_id', 'period_id')
                                        )

record_amount_association_table = db.Table('record_amount', 
                                            db.Column('record_id', db.Integer, db.ForeignKey('donation_record.id')),
                                            db.Column('amount_id', db.Integer, db.ForeignKey('donation_amount.id')),
                                            db.PrimaryKeyConstraint('record_id', 'amount_id')
                                        )
                                        

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    location = db.Column(db.Text, nullable=True, default="") 
    email = db.Column(db.Text, nullable=True, default="")
    hashed_password=db.Column(db.String(128))
    icon = db.Column(db.Text, nullable=True, default="user_default_1.png")
    donated_amount = db.Column(db.Integer, default=0)
    donate_records =  db.relationship('DonationRecord', backref='user', lazy=True)
    denote_plans = db.relationship('DonationPlan', backref='user', lazy=True)
    comments = db.relationship('ProjectComment', backref='user', lazy=True)

    @property
    def password(self):
      raise AttributeError('Password is not readable.')

    @password.setter
    def password(self,password):
      self.hashed_password=generate_password_hash(password)

    def verify_password(self,password):
      return check_password_hash(self.hashed_password,password)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(40), nullable=False)

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, default="")
    projects = db.relationship('Project', backref='organization', lazy=True) # one-to-many

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, default="")
    service_target = db.Column(db.Text, default="")
    funding_target = db.Column(db.Integer, default=0)
    funding_raised = db.Column(db.Integer, default=0)
    icon = db.Column(db.Text, nullable=True, default="project_default_1.png")
    before_date = db.Column(db.DateTime, nullable=True)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
    tags = db.relationship('Tag', secondary=project_tag_association_table, backref='projects')
    managers = db.relationship('User', secondary=project_manager_association_table, backref='managing_prjs') # many-to-many
    donations = db.relationship('DonationRecord', backref='project', lazy=True) # one-to-many
    donaters = db.relationship('User', secondary=project_donator_association_table, backref='donated_prjs') # many-to-many
    goals = db.relationship('ProjectGoal', backref='project', lazy=True) # one-to-many
    comments = db.relationship('ProjectComment', backref='project', lazy=True)

class ProjectGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    funding_required = db.Column(db.Integer, default=0)
    icon = db.Column(db.Text, nullable=True, default="goal_default_1.png")
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    progresses = db.relationship('GoalProgressPost', backref='goal', lazy=True) # one-to-many

class GoalProgressPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, default="")
    image = db.Column(db.Text, nullable=True, default="goal_default_1.png")
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    goal_id = db.Column(db.Integer, db.ForeignKey('project_goal.id'), nullable=False)

class GoalStage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.DateTime, nullable=True)

class DonationAmount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False, default=0)

class DonationPeriod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(40), nullable=False, default="")

class DonationPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    amount = db.relationship('DonationAmount', secondary=plan_amount_association_table, backref="donate_plan")
    period = db.relationship('DonationPeriod', secondary=plan_period_association_table, backref="donate_plan")
    records = db.relationship('DonationRecord', backref='plan', lazy=True) # one-to-many

class DonationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('donation_plan.id'))

class ProjectComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False, default="")
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    




