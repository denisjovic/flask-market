from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    # it must be named like this in order to check the actual username
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists, please try different username')
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists, please try different email')
    

    username = StringField(label=u'Username', validators=[Length(min=3, max=15), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=5), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[EqualTo('password'),DataRequired()])
    submit_data = SubmitField(label='Submit')


class LoginForm(FlaskForm):

    username = StringField(label=u'Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit_data = SubmitField(label='Sign in')


class PurchaseItemForm(FlaskForm):
    submit_data = SubmitField(label='Buy Item')


class SellItemForm(FlaskForm):
    submit_data = SubmitField(label='Sell Item')



