from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, TableForm
from flask_bootstrap import Bootstrap
from datetime import datetime
import cx_Oracle
from DBconnection import connection
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

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

        return render_template('graph.html', imgSrc=imgSrc)

@app.route('/join')
def join():
    return render_template('homeBase.html')


@app.route('/choose')
def choose():
    form_date = TableForm()
    return render_template('choose.html', title='choose', formdate=form_date)


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'destinholland' and form.password.data == '1234':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check username and password and try again.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account was created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True)

#
# admins = db.Table('admins',
#                   db.Column('book_id', db.Integer, db.ForeignKey('book_id'), primary_key=True),
#                   db.Column('user_id', db.Integer, db.ForeignKey('user_id'), primary_key=True)
# )
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.String(5))
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     # tables = db.relationship('Table', backref='user', lazy=True)
#
#     def __repr__(self):
#         return f"User('{ self.user_id }', '{ self.username }', '{ self.id }')"
#
#
# class Table(db.Model):
#     table_id = db.Column(db.Integer, primary_key=True)
#     table_name = db.Column(db.String(20), nullable=False)
#     members = db.Column(db.String(60), nullable=False)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     def __repr__(self):
#         return f"Table('{ self.table_id }', '{ self.username }')"