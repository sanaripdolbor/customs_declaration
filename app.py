from flask import Flask, request, redirect, url_for, render_template, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm
from flask import send_file
from werkzeug.utils import secure_filename
import io

from flask import send_file
from wtforms.validators import InputRequired, Length

from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import Length, AnyOf
import os
import numpy as np
import pandas as pd
from joblib import dump, load
import pycountry


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = '00000000'
db = SQLAlchemy(app)


class Declaration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hs_code = db.Column(db.Integer)  # Код ТНВЭД
    gross_weight = db.Column(db.Float)  # Вес брутто, кг
    net_weight = db.Column(db.Float)  # Вес нетто, кг
    customs_value = db.Column(db.Float)  # Таможенная стоимость, сом
    mto_code = db.Column(db.Integer)  # код МТО
    reference_gtd2 = db.Column(db.Integer)  # Справочный ГТД 2
    departure_country = db.Column(db.String(150))  # Страна отправления
    additional_units = db.Column(db.Float)  # Кол - во доп. ед
    customs_fees = db.Column(db.Float)  # Таможенные сборы
    customs_duties = db.Column(db.Float)  # Таможенные пошлины
    excise_tax = db.Column(db.Float)  # Акцизный налог
    vat = db.Column(db.Float)  # НДС
    total_charges = db.Column(db.Float)  # Всего по начис. платежам
    score_fraud0 = db.Column(db.Float, nullable=True)
    score_not_fraud1 = db.Column(db.Float, nullable=True)
    model_score = db.Column(db.Float, nullable=True)


class DeclarationForm(FlaskForm):
    country_names = [country.name for country in pycountry.countries]
    hs_code = StringField('Код ТНВЭД', validators=[InputRequired(message='Пожалуйста, заполните это поле'), Length(min=6, max=10, message='Должно быть введено 10 чисел')])
    gross_weight = FloatField('Вес брутто, кг', validators=[InputRequired(message='Пожалуйста, заполните это поле')])
    net_weight = FloatField('Вес нетто, кг', validators=[InputRequired(message='Пожалуйста, заполните это поле')])
    customs_value = FloatField('Таможенная стоимость, сом', validators=[InputRequired(message='Пожалуйста, заполните это поле')])
    mto_code = StringField('код МТО', validators=[InputRequired(message='Пожалуйста, заполните это поле'), Length(min=8, max=8, message='Должно быть введено 8 чисел')])
    reference_gtd2 = StringField('Справочный ГТД 2', validators=[InputRequired(message='Пожалуйста, заполните это поле')])
    departure_country = SelectField('Страна отправления', validators=[InputRequired(message='Пожалуйста, заполните это поле'), AnyOf(country_names)], choices=country_names)
    additional_units = FloatField('Кол - во доп. ед', validators=[InputRequired(message='Пожалуйста, заполните это поле')])
    customs_fees = FloatField('Таможенные сборы', validators=[InputRequired(message='Пожалуйста, заполните это поле')])
    customs_duties = FloatField('Таможенные пошлины', validators=[InputRequired(message='Пожалуйста, заполните это поле')])
    excise_tax = FloatField('Акцизный налог', validators=[InputRequired(message='Пожалуйста, заполните это поле')])
    vat = FloatField('НДС', validators=[InputRequired(message='Пожалуйста, заполните это поле')])
    total_charges = FloatField('Всего по начис. платежам', validators=[InputRequired(message='Пожалуйста, заполните это поле')])
    submit = SubmitField('Submit') 


@app.route('/', methods=['GET', 'POST'])
def home():
    form = DeclarationForm()
    try: 
        flash('Декларация была успешно принята', 'Принята')
        return render_template("home.html", form=form, score0=score0, score1=score1, pred=pred)
    except:
        return render_template("home.html", form=form, validation='это публичная версия')


@app.route('/view', methods=['GET','POST'])
def view():
    try:
        return redirect(url_for('/'))
    except:
        return "это публичная версия"
         


if __name__ == "__main__":
    app.run(debug=True)



    