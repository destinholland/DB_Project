from time import strftime
import os
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, QueryOneForm
from flask_bootstrap import Bootstrap
from datetime import datetime
import cx_Oracle
from DBconnection import connection
from graphs import GraphOne

app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
app.config['SECRET_KEY'] = '29b0ade026c5f7a2e831f73a73be8169'


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#
# db = SQLAlchemy(app)


@app.route('/account')
def account():
    return render_template('homeBase.html')


@app.route('/add')
def add():
    return render_template("homeBase.html")


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='home')


@app.route('/queryone', methods=['GET', 'POST'])
def queryOne():
    if os.path.exists("static/graph.png"):
        os.remove("static/graph.png")

    form = QueryOneForm(request.form)

    if form.validate():
        counties = ', '.join(form.counties.data)
        counties = '(' + counties + ')'
        print(counties)

        start_date = form.dStart.data.strftime('%m/%Y')
        print(start_date)

        end_date = form.dEnd.data.strftime('%m/%Y')
        print(end_date)

        GraphOne(request.form.getlist("counties"), request.form["dStart"], request.form["dEnd"], connection)

    return render_template('QueryOne.html', title='Query One', form=form)


if __name__ == '__main__':
    app.run(debug=True)
