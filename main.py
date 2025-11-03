from flask import Flask, url_for, render_template, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

import os
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir + 'data.sqlite')
db = SQLAlchemy(app)

class RegistrationForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    email = StringField("Email: ", )
    password = PasswordField("Password: ",)
    submit = SubmitField("Submit")

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    username = None
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ''

    #if name is in:
    #    return redirect(f'/user/{name}')

    return render_template('register.html', form=form, username=username)


if __name__ == '__main__':
    app.run(debug=True)