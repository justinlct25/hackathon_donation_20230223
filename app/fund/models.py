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
                                        

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    location = db.Column(db.Text, nullable=True, default="") 
    email = db.Column(db.Text, nullable=True, default="")
    hashed_password=db.Column(db.String(128))
    icon = db.Column(db.Text, nullable=True, default="user_default_1.png")

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
    donaters = db.relationship('User', secondary=project_donator_association_table, backref='donated_prjs') # many-to-many
    goals = db.relationship('ProjectGoal', backref='project', lazy=True) # one-to-many

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

class DonationAmount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False, default=0)

class DonationPeriod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(40), nullable=False, default="")

class DonationPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_id = db.Column(db.Integer, db.ForeignKey('donation_amount.id'), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('donation_period.id'), nullable=False)
    donater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    records = db.relationship('DonationRecord', backref='plan', lazy=True) # one-to-many

class DonationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_id = db.Column(db.Integer, db.ForeignKey('donation_amount.id'), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('donation_period.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('donation_plan.id'), nullable=False)





