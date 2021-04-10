from time import strftime

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, QueryOneForm
from flask_bootstrap import Bootstrap
from datetime import datetime
import cx_Oracle
# from DBconnection import connection
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import graphs

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

@app.route('/graph1', methods=[ 'GET', 'POST' ])
def graph1():

    if request.method == 'GET':
        return f"Invalid GET request"

    if request.method == 'POST':

        form_data = request.form

        whereClause = f"WHERE (name = '{form_data['counties']}')"
        orderByClause = "\nORDER BY rc4.County.name ASC, year ASC, mnum ASC\n"

        if form_data['start'] != '':
            whereClause = whereClause + f" AND (year >= {str(form_data['start'])[0:4]})"

        if form_data['end'] != '':
            whereClause = whereClause + f" AND (year <= {str(form_data['end'])[0:4]})"

        dbQuery = """
        SELECT name, year, month, Month_Average --Retrieves relevant information (Removes mnum that was used for ordering)
        FROM (
            SELECT rc4.County.name, year, month, Month_Average, mnum --Joins with county to get county names and orders data
            FROM (
                    SELECT countyFIPS, year, month, AVG(heat_value) as Month_Average, mnum --Calculates monthly averages
                    FROM (  SELECT t.*, EXTRACT(YEAR FROM HI_Date) as year, TO_CHAR(HI_Date, 'Month') as month, TO_CHAR(HI_Date, 'mm') as mnum --Extracts year and month
                            FROM rc4.Heat_Index t
                            )
                    GROUP BY countyFIPS, year, month, mnum
                    )
                NATURAL JOIN
                    rc4.County
        """

        dbQuery = dbQuery + whereClause + orderByClause + ")"

        cursor = connection.cursor()

        data = cursor.execute(dbQuery) # Cursor.execute returns an iterator that contains the results of the query

        x = []
        y = []

        for row in data:
            x.append( row[2] + str( row[1] ) )
            y.append( row[3] )

        plt.clf()
        plt.plot(x, y)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.xticks(rotation='vertical', fontsize=3)


        buf = BytesIO()
        plt.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        imgSrc = f"src=data:image/png;base64,{data}"

        return render_template('homeBase.html', imgSrc=imgSrc)

@app.route('/join')
def join():
    return render_template('homeBase.html')


@app.route('/choose')
def choose():
    form_date = TableForm()
    return render_template('choose.html', title='choose', formdate=form_date)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='home')


@app.route('/queryone', methods=['GET', 'POST'])
def queryOne():
    form = QueryOneForm(request.form)
    if form.validate():
        counties = ', '.join(form.counties.data)
        counties = '(' + counties + ')'
        print(counties)

        start_date = form.dStart.data.strftime('%m/%Y')
        print(start_date)

        end_date = form.dEnd.data.strftime('%m/%Y')
        print(end_date)


        return redirect(url_for('graph1'))
    return render_template('QueryOne.html', title='Query One', form=form)


if __name__ == '__main__':
    app.run(debug=True)