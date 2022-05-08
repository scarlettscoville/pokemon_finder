from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from ...models import User
import random
from jinja2.utils import markupsafe

# FORM SECTION
class LoginForm(FlaskForm):
    email = StringField('Email Address:', validators=[DataRequired(),Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email Address:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Register')

    r1=random.randint(1,1000)
    r2=random.randint(1001,2000)
    r3=random.randint(2001,3000)
    r4=random.randint(3001,4000)

    # https://avatars.dicebear.com/api/pixel-art

    r1_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/pixel-art/{r1}.svg" height="75px">')
    r2_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/pixel-art/{r2}.svg" height="75px">')
    r3_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/pixel-art/{r3}.svg" height="75px">')
    r4_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/pixel-art/{r4}.svg" height="75px">')

    icon = RadioField('Select an Avatar', validators=[DataRequired()],
        choices=[(r1, r1_img), (r2, r2_img), (r3, r3_img), (r4, r4_img)]
    )


    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()
        if same_email_user:
            raise ValidationError('Email is already in use.')

