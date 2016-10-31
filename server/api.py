from flask import jsonify, request
from config import *
from flask_user import login_required
from models import db
from models import *

##################################################
# USERS
##################################################
@app.route('/api/users', methods=['GET', 'PUT'])
def users():
  if request.method == 'GET':
    return get_users()
  elif request.method == 'PUT':
    return update_user()
  
def get_users():
  users = User.query.all()
  userlist = []
  for user in users:
    userlist.append(user.serialize())
  return jsonify(userlist)

def update_user():
  return ''

##################################################
# INSTITUTIONS
##################################################
@app.route('/api/institutions', methods=['GET', 'POST', 'PUT'])
def institutions():
  if request.method == 'GET':
    return get_institutions()
  elif request.method == 'POST':
    return post_institution()
  elif request.method == 'PUT':
    return update_institution()

def get_institutions():
  institutions = Institution.query.all()
  institutionlist = []
  for institution in institutions:
    institutionlist.append(institution.serialize())
  return jsonify(institutionlist)

def post_institution():
  return ''

def update_institution():
  return ''

##################################################
# TRANSACTIONS
##################################################
@app.route('/api/transactions', methods=['GET', 'POST'])
def transactions():
  if request.method == 'GET':
    return get_transactions()
  elif request.method == 'POST':
    return post_transaction()

def get_transactions():
  transactions = Transaction.query.all()
  transactionlist = []
  for transaction in transactions:
    transactionlist.append(transaction.serialize())
  return jsonify(transactionlist)

def post_transaction():
  return ''

##################################################
# COUNTRIES
##################################################
@app.route('/api/countries', methods=['GET', 'POST', 'PUT'])
def countries():
  if request.method == 'GET':
    return get_countries()
  elif request.method == 'POST':
    return post_country()
  elif request.method == 'PUT':
    return update_country()

def get_countries():
  countries = Country.query.all()
  countrylist = []
  for country in countries:
    countrylist.append(country.serialize())
  return jsonify(countrylist)

def post_country():
  return ''

def update_country():
  return ''
