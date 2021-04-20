from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, DecimalField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField, IntegerField
import datetime


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


class TotalTuplesForm(FlaskForm):
    submit = SubmitField("Count Tuples")

class QueryOneForm(FlaskForm):
    counties = SelectMultipleField('Counties', [validators.required()], choices = [
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
    dStart = DateField('Date Start (optional)', [validators.required()], format='%Y-%m-%d', default=datetime.date(1979, 5, 1))
    dEnd = DateField('Date End (optional)', [validators.required()], format='%Y-%m-%d', default=datetime.date(2016, 9, 1))
    submit = SubmitField('Submit')

# TODO put constraints on the date start and end date
class QueryTwoForm(FlaskForm):
    county = SelectField('County', [validators.required()], choices = [
        ('1', 'Alachua'),
        ('3', 'Baker'),
        ('5', 'Bay'),
        ('7', 'Bradford'),
        ('9', 'Brevard'),
        ('11', 'Broward'),
        ('13', 'Calhoun'),
        ('15', 'Charlotte'),
        ('17', 'Citrus'),
        ('19', 'Clay'),
        ('21', 'Collier'),
        ('23', 'Columbia'),
        ('27', 'De Soto'),
        ('29', 'Dixie'),
        ('31', 'Duval'),
        ('33', 'Escambia'),
        ('35', 'Flagler'),
        ('37', 'Franklin'),
        ('39', 'Gadsden'),
        ('41', 'Gilchrist'),
        ('43', 'Glades'),
        ('45', 'Gulf'),
        ('47', 'Hamilton'),
        ('49', 'Hardee'),
        ('51', 'Hendry'),
        ('53', 'Hernando'),
        ('55', 'Highlands'),
        ('57', 'Hillsborough'),
        ('59', 'Holmes'),
        ('61', 'Indian River'),
        ('63', 'Jackson'),
        ('65', 'Jefferson'),
        ('67', 'Lafayette'),
        ('69', 'Lake'),
        ('71', 'Lee'),
        ('73', 'Leon'),
        ('75', 'Levy'),
        ('77', 'Liberty'),
        ('79', 'Madison'),
        ('81', 'Manatee'),
        ('83', 'Marion'),
        ('85', 'Martin'),
        ('86', 'Miami-Dade'),
        ('87', 'Monroe'),
        ('89', 'Nassau'),
        ('91', 'Okaloosa'),
        ('93', 'Okeechobee'),
        ('95', 'Orange'),
        ('97', 'Osceola'),
        ('99', 'Palm Beach'),
        ('101', 'Pasco'),
        ('103', 'Pinellas'),
        ('105', 'Polk'),
        ('107', 'Putnam'),
        ('109', 'St Johns'),
        ('111', 'St Lucie'),
        ('113', 'Santa Rosa'),
        ('115', 'Sarasota'),
        ('117', 'Seminole'),
        ('119', 'Sumter'),
        ('121', 'Suwannee'),
        ('123', 'Taylor'),
        ('125', 'Union'),
        ('127', 'Volusia'),
        ('129', 'Wakulla'),
        ('131', 'Walton'),
        ('133', 'Washingto')])
    ethnicities = SelectMultipleField('Ethnicities', [validators.required()], choices = [
        ('1', 'White including Hispanic'),
        ('2', 'Black including Hispanic'),
        ('3', 'Asian/Pacific Islander including Hispanic'),
        ('4', 'American Indian/Alaskan Native including Hispanic'),
        ('5', 'Hispanic All Races'),
        ('6', 'All Non-White Races including Hispanic'),
        ('7', 'Other including Hispanic')])
    dStart = IntegerField('Start Year', [validators.required(), validators.NumberRange(min=1996, max=2017, message="Please input a value between %(min)s and %(max)s")], default=1996)
    dEnd = IntegerField('End Year', [validators.required(), validators.NumberRange(min=1997, max=2018, message="Please input a value between %(min)s and %(max)s")], default=2018)
    submit = SubmitField('Submit')

class QueryThreeForm(FlaskForm):
    counties = SelectMultipleField('Counties', [validators.required()], choices = [
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
    dStart = DateField('Date Start (optional)', [validators.required()], format='%Y-%m-%d', default=datetime.date(1979, 5, 1))
    dEnd = DateField('Date End (optional)', [validators.required()], format='%Y-%m-%d', default=datetime.date(2016, 9, 1))
    threshold = DecimalField('Heat Value Threshold (optional)', [validators.required()], default=85.0)
    submit = SubmitField('Submit')

class QueryFourForm(FlaskForm):
    counties = SelectMultipleField('Counties', [validators.required()], choices = [
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
    dStart = IntegerField('Start Year', [validators.required(), validators.NumberRange(min=2005, max=2016, message="Please input a value between %(min)s and %(max)s")], default=2005)
    dEnd = IntegerField('End Year', [validators.required(), validators.NumberRange(min=2005, max=2016, message="Please input a value between %(min)s and %(max)s")], default=2016)
    submit = SubmitField('Submit')



class QueryFiveForm(FlaskForm):
    counties = SelectMultipleField('Counties', [validators.required()], choices = [
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
    dStart = IntegerField('Start Year', [validators.required(), validators.NumberRange(min=1979, max=2016, message="Please input a value between %(min)s and %(max)s")], default=1979)
    dEnd = IntegerField('End Year', [validators.required(), validators.NumberRange(min=1979, max=2016, message="Please input a value between %(min)s and %(max)s")], default=2016)
    stdev = IntegerField('Number of Standard Deviations', [validators.required(), validators.NumberRange(min=1, max=10, message="Please input a value between %(min)s and %(max)s")], default=1)
    submit = SubmitField('Submit')