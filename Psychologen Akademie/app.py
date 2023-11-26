from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
import re


app = Flask(__name__)
app.app_context().push()

app.secret_key = "hi"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)

class Ratsuchende(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

class RatsuchendeForm(FlaskForm):
    text = StringField('text', validators=[DataRequired(), Length(min=2, max=220)])
    email= StringField('email', validators=[DataRequired(), Length(min=2, max=50)])

    agree = BooleanField('agree')

    submit = SubmitField('Speichern') 

def checkEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@app.route ('/', methods=['GET', 'POST'])
def index():

    form = RatsuchendeForm()
    if request.method == 'POST' and form.submit():
        text = request.form.get('text')
        email = request.form.get('email')
        agree = request.form.get('agree')

        if not checkEmail(email):
            flash('Bitte geben sie eine gültige emailadresse an.')
            return redirect(request.url)
        if not agree:
            flash('Bitte stimmen Sie den Bedingungen zu, um das Formular abzusenden.')
            return redirect(request.url)

        else:
            ratsuchende = Ratsuchende(text=form.text.data, email=form.email.data)
            db.session.add(ratsuchende)
            db.session.commit()
            flash('Formular erfolgreich abgesendet!')
            redirect('index.html')

    return render_template('index.html')

if __name__ =="__main__":
    db.create_all()
    app.run(debug=True)