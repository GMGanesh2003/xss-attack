from wtforms import EmailField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, EqualTo
from flask_wtf import FlaskForm

def my_required_field(form, field):
    if field.data == "":
        raise ValidationError('this filed is required')

class RegisterForm(FlaskForm):
    email = EmailField("Enter your email", validators=[my_required_field])
    username = StringField("Enter your name", validators=[my_required_field])
    password = PasswordField("Enter your password", validators=[my_required_field])
    password1 = PasswordField("Reenter your password", validators=[my_required_field, EqualTo('password', "password and reenter password must match")])
    submit = SubmitField("register")

class LoginForm(FlaskForm):
    email = StringField("Enter your email", validators=[my_required_field])
    password = PasswordField("Enter your password", validators=[my_required_field])
    submit = SubmitField("login")

class CommentForm(FlaskForm):
    title = StringField("Enter title", validators=[my_required_field])
    comment = TextAreaField("Enter content", validators=[my_required_field])
    submit = SubmitField("submit")

