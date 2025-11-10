from flask import Flask, url_for, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_required, login_user

#from flask_bootstrap import Bootstrap5

import os
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Login")

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    # Flask-Login required properties/methods
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    registerError = None

    existing_user = Users.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit() and not existing_user:
        user = Users(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    elif form.validate_on_submit():
        registerError = "Email already registered."

    return render_template('register.html', form=form, registerError=registerError)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    loginError = None
    
    if form.validate_on_submit():   
        user = Users.query.filter_by(email=form.email.data).first() 
        password = form.password.data
        
        if user and user.password == password:
            load_user(user.id)
            login_user(user)
            return redirect(url_for('protected'))      
        else:
            loginError = "Invalid email or password."

    return render_template('login.html', form=form, loginError=loginError)

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


if __name__ == '__main__':
    app.run(debug=True)