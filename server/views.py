from flask import render_template_string, render_template, jsonify
from config import *
from flask_user import login_required
from models import db
from models import *

@app.route('/')
# @login_required
def index():
  # return render_template_string("""
  #   {% extends "base.html" %}
  #   {% block content %}
  #       <h2>Members page</h2>
  #       <p>This page can only be accessed by authenticated users.</p><br/>
  #       <p><a href={{ url_for('user.register') }}>Home page</a> (anyone)</p>
  #       <p><a href={{ url_for('user.profile') }}>Members page</a> (login required)</p>
  #   {% endblock %}
  #   """)
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/api/users')
def get_users():
    users = User.query.all()
    userlist = []
    for user in users:
      userlist.append(user.serialize())
    return jsonify(userlist)

@app.route('/api/institutions')
def get_institutions():
    institutions = Institution.query.all()
    institutionlist = []
    for institution in institutions:
      institutionlist.append(institution.serialize())
    return jsonify(institutionlist)

@app.route('/api/transactions')
def get_transactions():
    transactions = Transaction.query.all()
    transactionlist = []
    for transaction in transactions:
      transactionlist.append(transaction.serialize())
    return jsonify(transactionlist)

@app.route('/api/countries')
def get_countries():
    countries = Country.query.all()
    countrylist = []
    for country in countries:
      countrylist.append(country.serialize())
    return jsonify(countrylist)
