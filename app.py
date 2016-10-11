import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# FlaskUser: provides login and password and stuff
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

class ConfigClass(object):
  SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/test.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False')
  SECRET_KEY = os.getenv('SECRET_KEY', 'SOMETHING')
  USER_APP_NAME = 'Tallodfasfires'

def create_app():
  app = Flask(__name__)
  app.config.from_object(__name__+'.ConfigClass')
  db = SQLAlchemy(app)

  class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    country = db.Column(db.String(50)) # should probably be a FOREIGN KEY

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    # FlaskUser defined field (necessary?) confirmed_at = db.Column(db.DateTime())

    # User information
    # FlaskUser defined field (necessary?) active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    institution = db.Column(db.String(80), nullable=False) # should also probably be a FOREIGN KEY
    prefix = db.Column(db.String(8))
    first_name = db.Column(db.String(50), nullable=False, server_default='')
    last_name = db.Column(db.String(127), nullable=False, server_default='')
    position = db.Column(db.String(127))
    phone = db.Column(db.Integer()) # maybe there's a special type in SQLAlchemy for phone number (revisit later please)

    # a list of transaction FOREIGN keys, pointing to the table below
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')

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

  db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
  user_manager = UserManager(db_adapter, app)     # Initialize Flask-User

  @app.route('/user/sign-in')
  @login_required
  def hello_world():
    return render_template_string("""
      {% extends "base.html" %}
      {% block body %}
          <h2>Members page</h2>
          <p>This page can only be accessed by authenticated users.</p><br/>
          <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
          <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
      {% endblock %}
      """)
  return app


if __name__=='__main__':
  app = create_app()
  app.run(host='127.0.0.1', port=5000, debug=True)
