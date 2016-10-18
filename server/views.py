from flask import render_template_string
from config import *
from flask_user import login_required

@app.route('/')
@login_required
def hello_world():
  return render_template_string("""
    {% extends "base.html" %}
    {% block content %}
        <h2>Members page</h2>
        <p>This page can only be accessed by authenticated users.</p><br/>
        <p><a href={{ url_for('user.register') }}>Home page</a> (anyone)</p>
        <p><a href={{ url_for('user.profile') }}>Members page</a> (login required)</p>
    {% endblock %}
    """)
