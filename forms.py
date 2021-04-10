from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class QueryOneForm(FlaskForm):
    counties = SelectMultipleField('Counties', choices = [
        ('Alachua', 'Alachua'),
        ('Baker', 'Baker'),
        ('Bay', 'Bay'),
        ('Bradford', 'Bradford'),
        ('Brevard', 'Brevard'),
        ('Broward', 'Broward'),
        ('Calhoun', 'Calhoun'),
        ('Charlotte', 'Charlotte'),
        ('Citrus', 'Citrus'),
        ('Clay', 'Clay'),
        ('Collier', 'Collier'),
        ('Columbia', 'Columbia'),
        ('De Soto', 'De Soto'),
        ('Dixie', 'Dixie'),
        ('Duval', 'Duval'),
        ('Escambia', 'Escambia'),
        ('Flagler', 'Flagler'),
        ('Franklin', 'Franklin'),
        ('Gadsden', 'Gadsden'),
        ('Gilchrist', 'Gilchrist'),
        ('Glades', 'Glades'),
        ('Gulf', 'Gulf'),
        ('Hamilton', 'Hamilton'),
        ('Hardee', 'Hardee'),
        ('Hendry', 'Hendry'),
        ('Hernando', 'Hernando'),
        ('Highlands', 'Highlands'),
        ('Hillsborough', 'Hillsborough'),
        ('Holmes', 'Holmes'),
        ('Indian River', 'Indian River'),
        ('Jackson', 'Jackson'),
        ('Jefferson', 'Jefferson'),
        ('Lafayette', 'Lafayette'),
        ('Lake', 'Lake'),
        ('Lee', 'Lee'),
        ('Leon', 'Leon'),
        ('Levy', 'Levy'),
        ('Liberty', 'Liberty'),
        ('Madison', 'Madison'),
        ('Manatee', 'Manatee'),
        ('Marion', 'Marion'),
        ('Martin', 'Martin'),
        ('Miami-Dade', 'Miami - Dade'),
        ('Monroe', 'Monroe'),
        ('Nassau', 'Nassau'),
        ('Okaloosa', 'Okaloosa'),
        ('Okeechobee', 'Okeechobee'),
        ('Orange', 'Orange'),
        ('Osceola', 'Osceola'),
        ('Palm Beach', 'Palm Beach'),
        ('Pasco', 'Pasco'),
        ('Pinellas', 'Pinellas'),
        ('Polk', 'Polk'),
        ('Putnam', 'Putnam'),
        ('St Johns', 'St Johns'),
        ('St Lucie', 'St Lucie'),
        ('Santa Rosa', 'Santa Rosa'),
        ('Sarasota', 'Sarasota'),
        ('Seminole', 'Seminole'),
        ('Sumter', 'Sumter'),
        ('Suwannee', 'Suwannee'),
        ('Taylor', 'Taylor'),
        ('Union', 'Union'),
        ('Volusia', 'Volusia'),
        ('Wakulla', 'Wakulla'),
        ('Walton', 'Walton'),
        ('Washington', 'Washington')])
    dStart = DateField('Date Start', format='%Y-%m-%d')
    dEnd = DateField('Date End', format='%Y-%m-%d')
    submit = SubmitField('Submit')

# TODO put constraints on the date start and end date
