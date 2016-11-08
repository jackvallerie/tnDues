from flask import render_template_string, render_template, jsonify, request
from .config import *
from flask_user import login_required
from .models import db
from .models import *
import flask_login
import stripe

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

@app.route('/stripe', methods = ['GET'])
def stripe():
    return render_template('stripe.html', key=stripe_keys['publishable_key'])
  

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 50000
    customer = stripe.Customer.create(
        email ='customer@example.com',
        source = request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer = customer.id,
        amount = amount,
        currency = 'usd',
        description = 'Flask Charge'
    )
    return render_template('charge.html', amount=amount)


