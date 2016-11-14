### (From my limited understanding) how flask-login works

Note from base.html, register links to user.register
-> Refer to /env/lib/python3.5/site-packages/flask_user/templates/flask_user/register.html

Similarly, sign in links to user.login => This renders a login page from
-> Refer to /env/lib/python3.5/site-packages/flask_user/templates/flask_user/...

Flask already creates a link among all of these pages. One option to make our lives easier
is to find the places where these pages come from/ how they get rendered and change them
