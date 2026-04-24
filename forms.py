from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange, Length, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = SelectField('Remember Me', choices=[('yes', 'Yes'), ('no', 'No')], default='no')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    farm_size = FloatField('Farm Size (hectares)', validators=[NumberRange(min=0)])
    location = StringField('Location', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Length(max=15)])

class SoilDataForm(FlaskForm):
    ph = FloatField('pH Level', validators=[DataRequired(), NumberRange(min=0, max=14)])
    nitrogen = FloatField('Nitrogen (mg/kg)', validators=[DataRequired(), NumberRange(min=0)])
    phosphorus = FloatField('Phosphorus (mg/kg)', validators=[DataRequired(), NumberRange(min=0)])
    potassium = FloatField('Potassium (mg/kg)', validators=[DataRequired(), NumberRange(min=0)])
    moisture = FloatField('Moisture (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
