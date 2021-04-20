from time import strftime
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, TotalTuplesForm, QueryOneForm, QueryTwoForm, QueryThreeForm, QueryFourForm
from flask_bootstrap import Bootstrap
from datetime import datetime
import cx_Oracle
from DBconnection import connection
from graphs import GraphOne, GraphTwo, GraphThree, GraphFour

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
    
    form = TotalTuplesForm(request.form)

    tupleNum = ''

    if request.method == 'POST':

        dbQuery = """
        SELECT SUM(NUM)
        FROM (
            SELECT COUNT(*) AS NUM
            FROM RC4.Average_uv_irradiance
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.COUNTY
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.DEMOGRAPHIC
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.ETHNICITY
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.HEAT_INDEX
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.HEAT_MORTALITIES
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.HEAT_RELATED_HOSPITALIZATIONS
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.LABORATORY
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.MEASUREMENT_UNIT
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.MELANOMA_CASES
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.MORTALITIES
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.PRECIPITATION
            UNION ALL
            SELECT COUNT(*) AS NUM
            FROM RC4.STATE
        )
        """

        cursor = connection.cursor()

        data = cursor.execute(dbQuery)

        tupleNum = next(data)[0]

    return render_template('home.html', title='home', form=form, tupleNum=tupleNum)


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

@app.route('/querytwo', methods=['GET', 'POST'])
def queryTwo():

    form = QueryTwoForm(request.form)

    if request.method == 'POST' and form.validate():
        print(request.form["county"])
        imgSrc = GraphTwo(request.form["county"], request.form.getlist("ethnicities"), request.form["dStart"], request.form["dEnd"], connection)
        return render_template('QueryTwo.html', title='Query Two', form=form, imgSrc=imgSrc)


    imgSrc = "src=static/defaultgraph.png"
    return render_template('QueryTwo.html', title='Query Two', form=form, imgSrc=imgSrc)

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
