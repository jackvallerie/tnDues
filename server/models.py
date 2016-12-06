from .config import *
from flask_user import UserMixin, SQLAlchemyAdapter, UserManager
from flask_user.forms import RegisterForm
from flask_wtf import Form
from wtforms import *



class User(db.Model, UserMixin):
  __tablename__='User'
  id = db.Column(db.Integer, primary_key=True)

  # User authentication information
  username = db.Column(db.String(50), nullable=False, unique=True)
  password = db.Column(db.String(255), nullable=False, server_default='')
  reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
  country = db.Column(db.String(50)) # should probably be a FOREIGN KEY

  # User email information
  email = db.Column(db.String(255), nullable=False, unique=True)

  confirmed_at = db.Column(db.DateTime())

  # User information
  institution = db.Column(db.String(80), nullable=False) # should also probably be a FOREIGN KEY
  prefix = db.Column(db.String(8))
  first_name = db.Column(db.String(50), nullable=False, server_default='')
  last_name = db.Column(db.String(127), nullable=False, server_default='')
  position = db.Column(db.String(127))
  phone = db.Column(db.Integer()) # maybe there's a special type in SQLAlchemy for phone number (revisit later please)
  is_enabled = db.Column(db.Boolean(), nullable=False, default=False)

  # Relationships
  roles = db.relationship('Role', secondary='user_roles',
          backref=db.backref('users', lazy='dynamic'))

  def is_active(self):
    return self.is_enabled

  def serialize(self):
    return {
      "id": self.id,
      "username": self.username,
      # "password": self.password,
      "reset_password_token": self.reset_password_token,
      "country": self.country,
      "email": self.email,
      "confirmed_at": self.confirmed_at,
      "institution": self.institution,
      "prefix": self.prefix,
      "first_name": self.first_name,
      "last_name": self.last_name,
      "position": self.position,
      "phone": self.phone,
      "is_enabled": self.is_enabled
    }

  # a list of transaction FOREIGN keys, pointing to the table below
  # transactions = db.relationship('Transaction', backref='user', lazy='dynamic')

# Define the Role data model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    # label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes

# Define the UserRoles association model
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('User.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class Transaction(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  amt = db.Column(db.Float())
  user_id = db.Column(db.Integer(), db.ForeignKey('User.id'))
  def serialize(self):
    return {
      "id": self.id,
      "amt": self.amt,
      "user_id": self.user_id
    }

class Country(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(40), unique=True)
  price = db.Column(db.Float())
  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "price": self.price
    }

class Institution(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  def serialize(self):
    return {
      "id": self.id,
      "name": self.name
    }

class CountryForm(Form):
  name  = StringField('Country Name')
  price = DecimalField('Cost')
  submit = SubmitField()

class InstitutionForm(Form):
  name = StringField('Full Institution Name')
  submit = SubmitField()

class MyRegisterForm(RegisterForm):
    first_name  = StringField('First name')
    last_name   = StringField('Last name')
    insts = map(lambda obj: (obj.name, obj.name), Institution.query.all())
    institution = SelectField('Institution', choices=insts)


db.create_all() # create all the models

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, UserClass=User) # Register the User model
user_manager = UserManager(db_adapter, app, register_form=MyRegisterForm)

# Add a User Admin
# to add a new admin to your database:
# create a user with the user name user007, that user will become an admin

if not Role.query.filter(Role.name=='admin').first():
  role1 = Role(name='admin')
  db.session.add(role1)
  db.session.commit()

# if not UserRoles.query.filter(UserRoles.role_id==1).first():
if not User.query.filter(User.username=='user007').first():
  user1 = User(username='user007', password=user_manager.hash_password('Password1'), reset_password_token = '',
              email='tuftstalloiresnetwork@gmail.com', institution = 'Tufts', first_name = 'Admin', 
              last_name = 'ADMIN', is_enabled = True)
  #user1 =  User.query.filter(User.username=='user007').first() 
  user1.roles.append(Role.query.filter(Role.name=='admin').first())
  db.session.add(user1)
  db.session.commit()


