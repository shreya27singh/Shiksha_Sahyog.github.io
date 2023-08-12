from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email
import os

app = Flask(__name__)

# Set a secret key for CSRF protection
app.config['SECRET_KEY'] = os.urandom(24)  # Generates a random secret key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sponsorship.db'
db = SQLAlchemy(app)

class Sponsorship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

class SponsorshipForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    amount = IntegerField('Sponsorship Amount', validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sponsor', methods=['GET', 'POST'])
def sponsor():
    form = SponsorshipForm()
    if form.validate_on_submit():
        new_sponsorship = Sponsorship(
            name=form.name.data,
            email=form.email.data,
            amount=form.amount.data
        )
        db.session.add(new_sponsorship)
        db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('sponsor.html', form=form)

@app.route('/thank_you')
def thank_you():
    return "Thank you for sponsoring a student!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
