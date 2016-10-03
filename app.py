from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# DY: We should really talk through these (are they the right data?)
class User(db.Model):
  # Do we need both id and username? We should probably only have one ID,
  # that should be the login name
  id = db.Column(db.String(16), primary_key=True)
  username = db.Column(db.String(80), unique=True)
  country = db.Column(db.String(50)) # should probably be a FOREIGN KEY
  institution = db.Column(db.String(80)) # should also probably be a FOREIGN KEY
  firstName = db.Column(db.String(16))
  lastName = db.Column(db.String(24))
  prefix = db.Column(db.String(8))
  email = db.Column(db.String(120), unique=True)
  position = db.Column(db.String(40))
  phone = db.Column(db.Integer()) # maybe there's a special type for phone number (revisit later please)
  paid = db.Column(db.Boolean())
  # we don't want the transaction to be in here, because it'd be a list in a table (not good to work with). Instead, we lookup using the class below.

class Transaction(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(80), unique=True)
  country = db.Column(db.String(50)) # should probably be a FOREIGN KEY
  institution = db.Column(db.String(80)) # should also probably be a FOREIGN KEY
  firstName = db.Column(db.String(16))
  lastName = db.Column(db.String(24))
  prefix = db.Column(db.String(8))
  email = db.Column(db.String(120), unique=True)
  position = db.Column(db.String(40))
  phone = db.Column(db.Integer()) # maybe there's a special type for phone number (revisit later please)  

class Country(db.Model):
  id = db.Column(db.String(50), primary_key=True)
  price = db.Column(db.Float())

@app.route('/')
def hello_world():
    return 'Hello, World!'
    