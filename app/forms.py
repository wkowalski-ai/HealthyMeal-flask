from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class DeleteRecipeForm(FlaskForm):
    pass

class RecipeForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired(), Length(max=140)])
    content = StringField('Treść przepisu', validators=[DataRequired()])
    submit = SubmitField('Zapisz przepis')

class ProfileForm(FlaskForm):
    allergies = TextAreaField('Alergie', render_kw={"rows": 2, "placeholder": "Np. orzechy, mleko..."})
    excluded_products = TextAreaField('Produkty wykluczone', render_kw={"rows": 2, "placeholder": "Czego nie możesz jeść?"})
    favorite_products = TextAreaField('Ulubione produkty', render_kw={"rows": 2, "placeholder": "Co lubisz najbardziej?"})
    submit = SubmitField('Zapisz profil')
