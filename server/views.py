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




########### FLASK LOGIN FACILITY ##############

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# https://flask-login.readthedocs.io/en/latest/
# Note that the class User needs to implement a number of methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

@app.route("/settings")
@login_required
def settings():
    pass
########## TESTING PURPOSE ##########

@app.route('/user/sign-in')
@login_required
def thing():
  return render_template('programs.html')
