from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email,DataRequired, EqualTo, ValidationError
from .models import User


class SearchForm(FlaskForm):
                    #field name = datatypefield('label', validators = [LIST of validators])
    name = StringField('Enter the pokemon you would like to see!',validators=[DataRequired()])
    
    submit = SubmitField('Show me!')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Password',validators=[DataRequired()])

    email = StringField('Email Address',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Repeat Password',validators=[DataRequired(), EqualTo ('password' , message='Passwords must match!')])
    submit = SubmitField('Register')

    def validate_email(form , field):
        same_email_user = User.query.filter_by(email = field.data).first()
        if same_email_user:
            raise ValidationError('Email Is Already In Use !')


class LoginForm(FlaskForm):
                    #field name = datatypefield('label', validators = [LIST of validators])
    email = StringField('Email Address',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')