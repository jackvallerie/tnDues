from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class ConfigClass(object):
  SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/test.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False')
  SECRET_KEY = os.getenv('SECRET_KEY', 'SOMETHING')
  # CSRF_ENABLED = True

  USER_APP_NAME = 'The Talloires Network'
  # Flask-Mail settings 
  MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'tuftstalloiresnetwork@gmail.com')
  MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'Talloires1')
  MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '"The Talloires Network" <noreply@example.com>')
  MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
  MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
  MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))

app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')
db = SQLAlchemy(app)
mail = Mail(app)

