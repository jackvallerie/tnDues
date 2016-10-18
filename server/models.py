from config import *
from flask_user import UserMixin, SQLAlchemyAdapter, UserManager
from flask_user.forms import RegisterForm
from wtforms import StringField, SubmitField, validators


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)

  # User authentication information
  username = db.Column(db.String(50), nullable=False, unique=True)
  password = db.Column(db.String(255), nullable=False, server_default='')
  reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
  country = db.Column(db.String(50)) # should probably be a FOREIGN KEY

  # User email information
  email = db.Column(db.String(255), nullable=False, unique=True)

  confirmed_at = db.Column(db.DateTime())

  # User information
  institution = db.Column(db.String(80), nullable=False) # should also probably be a FOREIGN KEY
  prefix = db.Column(db.String(8))
  first_name = db.Column(db.String(50), nullable=False, server_default='')
  last_name = db.Column(db.String(127), nullable=False, server_default='')
  position = db.Column(db.String(127))
  phone = db.Column(db.Integer()) # maybe there's a special type in SQLAlchemy for phone number (revisit later please)
  is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
  def is_active(self):
    return self.is_enabled

  # a list of transaction FOREIGN keys, pointing to the table below
  # transactions = db.relationship('Transaction', backref='user', lazy='dynamic')

class MyRegisterForm(RegisterForm):
  first_name = StringField('First name')
  last_name  = StringField('Last name')
  institution  = StringField('Institution')


class Transaction(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  amt = db.Column(db.Float())
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Country(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(40))
  price = db.Column(db.Float())

class Institution(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), nullable=False)

db.create_all() # create all the models

db_adapter = SQLAlchemyAdapter(db, UserClass=User)        # Register the User model
user_manager = UserManager(db_adapter, app, register_form=MyRegisterForm)
