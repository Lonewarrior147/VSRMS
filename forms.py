from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from models import User


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    name = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Name"})
    phone = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Phone"})
    address = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Address"})

    submit = SubmitField("Register")

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError("Account already exists. Please Login")


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")
