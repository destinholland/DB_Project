from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, TableForm
from flask_bootstrap import Bootstrap
from datetime import datetime

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
    import cx_Oracle
    from DBconnection import connection

    cursor = connection.cursor()

    data = cursor.execute("SELECT * FROM RC4.Heat_Index FETCH FIRST 1 ROWS ONLY") # Cursor.execute returns an iterator that contains the results of the query
    data = next( data ) # next( data ) gets the first row in the query result

    return render_template('homeBase.html', data=data)


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