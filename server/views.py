from flask import render_template_string, render_template, jsonify, request
from .config import *
from flask_user import login_required, roles_required
from .models import *
import flask_login
import stripe as st
from wtforms.ext.sqlalchemy.orm import model_form


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/programs', methods=['GET'])
def programs():
    return render_template('programs.html')

chargeAmount = 700

@app.route('/payment', methods=['GET'])
@login_required
def stripe():
    return render_template('payment.html', key=stripe_keys['publishable_key'],
                            amount = chargeAmount)

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    st.api_key = stripe_keys['secret_key']

    customer = st.Customer.create(
        email ='customer@example.com',
        source = request.form['stripeToken']
    )
    try:
        charge = st.Charge.create(
            customer = customer.id,
            amount = chargeAmount,
            currency = 'usd',
            description = 'Taillores Conference Charge'
        )
        return render_template('charge.html', amount=chargeAmount)
    except st.error.CardError as e:
        # Card declined
        print ("Ooops, card declined!")

################################################################
# ADMIN SETTINGS 
# Shown in the UI for ONLY admin users (add roles required)
################################################################
@app.route('/admin', methods=['GET', 'POST', 'PUT'])
@roles_required('admin')
def admin():
  if request.method == 'GET':
    return render_template('programs.html')


@app.route('/settings/countries', methods=['GET', 'POST', 'PUT'])
@roles_required('admin')
def countries():
  if request.method == 'GET':
    myform = CountryForm(request.form)
    return render_template('admin_settings/country.html', form=myform)
  else:
    return upsert_country()

def upsert_country():
  country = Country.query.filter_by(name=request.form['name']).first()
  if country is not None:
    country.price = request.form['price']
    db.session.commit()
  else:
    country = Country()
    country.name = request.form['name']
    country.price = request.form['price']
    db.session.add(country)
    db.session.commit()
  myform = CountryForm(request.form)
  return render_template('admin_settings/country.html', form=myform)

@app.route('/settings/institutions', methods=['GET', 'POST', 'PUT'])
@roles_required('admin')
def settings_institutions():
  if request.method == 'GET':
    myform = InstitutionForm(request.form)
    return render_template('admin_settings/institution.html', form=myform)
  else:
    return upsert_institution()

def upsert_institution():
  inst = Institution.query.filter_by(name=request.form['name']).first()
  if inst is None and request.form['name'] != '':
    inst = Institution()
    inst.name = request.form['name']
    db.session.add(inst)
    db.session.commit()
  myform = InstitutionForm()
  return render_template('admin_settings/institution.html', form=myform)
