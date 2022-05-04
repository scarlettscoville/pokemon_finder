from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

# FORM SECTION
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PokemonForm(FlaskForm):
    name = StringField("Pokemon Name", validators = [DataRequired()])
    submit = SubmitField("Submit")