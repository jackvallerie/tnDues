from flask import jsonify, request
from config import *
from flask_user import login_required
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

# get all the users
def get_users():
  users = User.query.all()
  userlist = []
  for user in users:
    userlist.append(user.serialize())
  return jsonify(userlist)

# update a user's information
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

# get all institutions
def get_institutions():
  institutions = Institution.query.all()
  institutionlist = []
  for institution in institutions:
    institutionlist.append(institution.serialize())
  return jsonify(institutionlist)

# insert a new institution
def post_institution():
  newinst = Institution()
  # do error checking! (might not exist)
  newinst.name = request.form['name']
  db.session.add(newinst)
  db.session.commit()
  return jsonify(newinst.serialize())

# update an existing institution
def update_institution():
  inst = Institution.query.get(request.form['id'])
  newname = request.form['name']
  if newname:
    inst.name = newname
  db.session.commit()
  return jsonify(inst.serialize())

##################################################
# TRANSACTIONS
##################################################
@app.route('/api/transactions', methods=['GET', 'POST'])
def transactions():
  if request.method == 'GET':
    return get_transactions()
  elif request.method == 'POST':
    return post_transaction()

# get all transactions
def get_transactions():
  transactions = Transaction.query.all()
  transactionlist = []
  for transaction in transactions:
    transactionlist.append(transaction.serialize())
  return jsonify(transactionlist)

# insert a new transaction
def post_transaction():
  newtrans = Transaction()
  newtrans.amt = request.form['amt']
  newtrans.user_id = request.form['user_id']
  db.session.add(newtrans)
  db.session.commit()
  return jsonify(newtrans.serialize())

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
  newcountry = Country()
  newcountry.name = request.form['name']
  newcountry.price = request.form['price']
  db.session.add(newcountry)
  db.session.commit()
  return jsonify(newcountry.serialize())

def update_country():
  country = Country.query.get(request.form['id'])
  newname = request.form['name']
  newprice = request.form['price']
  if newname:
    country.name = newname
  if newprice:
    country.price = newprice
  return jsonify(country.serialize())
