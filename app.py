from time import strftime
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, QueryOneForm, QueryThreeForm, QueryFourForm
from flask_bootstrap import Bootstrap
from datetime import datetime
import cx_Oracle
from DBconnection import connection
from graphs import GraphOne, GraphThree, GraphFour

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

    form = QueryOneForm(request.form)

    """ if form.validate():
        counties = ', '.join(form.counties.data)
        counties = '(' + counties + ')'
        print(counties)

        start_date = form.dStart.data.strftime('%m/%Y')
        print(start_date)

        end_date = form.dEnd.data.strftime('%m/%Y')
        print(end_date) """


    if request.method == 'POST' and form.validate():
        imgSrc = GraphOne(request.form.getlist("counties"), request.form["dStart"], request.form["dEnd"], connection)
        return render_template('QueryOne.html', title='Query One', form=form, imgSrc=imgSrc)


    imgSrc = "src=static/defaultgraph.png"
    return render_template('QueryOne.html', title='Query One', form=form, imgSrc=imgSrc)

@app.route('/querythree', methods=['GET', 'POST'])
def queryThree():

    form = QueryThreeForm(request.form)

    """ if form.validate():
        counties = ', '.join(form.counties.data)
        counties = '(' + counties + ')'
        print(counties)

        start_date = form.dStart.data.strftime('%m/%Y')
        print(start_date)

        end_date = form.dEnd.data.strftime('%m/%Y')
        print(end_date) """


    if request.method == 'POST' and form.validate():
        imgSrc = GraphThree(request.form.getlist("counties"), request.form["dStart"], request.form["dEnd"], request.form["threshold"], connection)
        return render_template('QueryThree.html', title='Query Three', form=form, imgSrc=imgSrc)


    imgSrc = "src=static/defaultgraph.png"
    return render_template('QueryThree.html', title='Query Three', form=form, imgSrc=imgSrc)

@app.route('/queryfour', methods=['GET', 'POST'])
def queryFour():

    form = QueryFourForm(request.form)

    """ if form.validate():
        counties = ', '.join(form.counties.data)
        counties = '(' + counties + ')'
        print(counties)

        start_date = form.dStart.data.strftime('%m/%Y')
        print(start_date)

        end_date = form.dEnd.data.strftime('%m/%Y')
        print(end_date) """


    if request.method == 'POST' and form.validate():
        imgSrc = GraphFour(request.form.getlist("counties"), request.form["dStart"], request.form["dEnd"], connection)
        return render_template('QueryFour.html', title='Query Four', form=form, imgSrc=imgSrc)

    imgSrc = "src=static/defaultgraph.png"
    return render_template('QueryFour.html', title='Query Four', form=form, imgSrc=imgSrc)

if __name__ == '__main__':
    app.run(debug=True)
