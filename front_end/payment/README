### PAYMENT
The general flow is

User keys in credit card info -> sends to Stripe (Stripe does all the validation for us)
-> Stripe sends back a token -> front end sends this token to back end -> back end sends charge
request to Stripe

## FRONT END:

- There will be a PublishableKey that stripe uses to recognize the origin of the
website where card info comes from (only our website can have this key)

<script type="text/javascript">
  Stripe.setPublishableKey('pk_test_6pRNASCoBOKtIshFeQd4XMUh');
</script>

- User keys in card information. Some functions in Stripe.js send the card info
to the server

Stripe.card.createToken(ccData, function stripeResponseHandler(status, response)

The stripe server returns (response text)
{
  id: "tok_u5dg20Gra", // Token identifier
  card: {...}, // Dictionary of the card used to create the token
  created: 1475543791, // Timestamp of when token was created
  currency: "usd", // Currency that the token was created in
  livemode: false, // Whether this token was created with a live API key
  object: "token", // Type of object, always "token"
  used: false // Whether this token has been used
}

We then need to send the token identifier to the server.
$.post('/account/stripe_card_token', {
        token: token
    })


- In the server, we can charge the user with the given card token. Stripe has
detailed documentation on how to work with flask.
https://stripe.com/docs/checkout/flask

import os
from flask import Flask, render_template, request
import stripe

stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY'] # This is the publishable key on our website
}

stripe.api_key = stripe_keys['secret_key'] # This secret key is only in our server

# Assuming our api url is /charge. The POST data is the card token (generated
by stripe)

@app.route('/charge', methods=['POST'])
def charge():
    amount = 500 # Amount of money being charged

    customer = stripe.Customer.create(
        email='customer@example.com', # Can get the email from the user
        source=request.form['token'] # Get the token
    )

    charge = stripe.Charge.create( # The actual charges are being made here
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge' # Description
    )

    return render_template('charge.html', amount=amount)
    # This is only to send back to the front end saying "You've been charged"
