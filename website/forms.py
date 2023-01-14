from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from website.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, new_username):
        user= User.query.filter_by(username = new_username.data).first()
        if user:
            raise ValidationError('An account has already been registered with this username. Please choose a different username.')
    def validate_email_address(self, new_email):
        email_address = User.query.filter_by(email_address = new_email.data).first()
        if email_address:
            raise ValidationError('An account has already been registered with this email address. Please choose a different address.')
    username = StringField(label = "User Name:", validators = [Length(min=2, max=25), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6),DataRequired()])
    password_confirm = PasswordField(label='Please Confirm your Password: ', validators=[Length(min=6), DataRequired(), EqualTo('password')])
    email_address = StringField(label='Email Address:', validators= [Email(), DataRequired()])
    submit = SubmitField(label='Register')
    

class LoginForm(FlaskForm):
    username = StringField(label = "User Name:", validators = [DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class BudgetForm(FlaskForm):
    budget = StringField(label="Budget", validators=[DataRequired()])
    submit = SubmitField(label='Submit')

class WeekForm(FlaskForm):
    submit = SubmitField(label='Select')
class ExpenseListForm(FlaskForm):
    submit = SubmitField(label="Select")
