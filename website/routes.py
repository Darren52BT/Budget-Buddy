from website import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from website.models import User, Budget, Week
from website.forms import RegisterForm, LoginForm, BudgetForm
from website import db
from flask_login import login_user, logout_user, login_required, current_user

#-----------------LANDING---------------------------#
@app.route('/')
def landing_page():
    return render_template("landing.html")

#-----------------HOME---------------------------#
@app.route('/home/')
def home_page():
    return render_template("home.html")


#-----------------REGISTER---------------------------#
@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    #registration validation, if successful, return to home page after
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password = form.password.data, email_address=form.email_address.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"You have successfully registered as {new_user.username}! Good Luck on budgeting successfully")
        #return home
        return redirect(url_for('home_page'))

    if form.errors != {}: # if validation wasn't successful, present errors
        for  msg in form.errors.values():
            flash(f'There was an error with registration: {msg}')
    
    #direct user to register page
    return render_template('register.html', form=form)

#-----------------LOGIN---------------------------#
@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    #login validation, if successful, return to home page after
    if form.validate_on_submit():
        return_user = User.query.filter_by(username = form.username.data).first()
        if return_user and return_user.check_password(pass_attempt = form.password.data):
            login_user(return_user)
            flash(f'You have successfully logged in as {return_user.username}')
            return redirect(url_for('home_page'))
        else:
            flash('Sorry, the username and password does not match an account. Please try again.')
    return render_template('login.html', form = form)


#-----------------LOGOUT ------------------------#
@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have logged out successfully. Remember to keep track of your budget!')
    return redirect(url_for('home_page'))

#-----------------BUDGET FORM --------------------------#
@app.route('/budget-form', methods=['GET', 'POST'])
@login_required
def budget_form_page():
    form = BudgetForm()
    if form.validate_on_submit():       
        new_week = Week(owner=current_user.id)
        new_week.budget = Budget(weekOwner_Id=new_week.id, budget = form.budget.data, budgetLeft = form.budget.data)      

        db.session.add(new_week)
        db.session.commit()
        flash(f'You have successfully created a week {new_week.id} with a budget of{new_week.budget.budget}')
        return redirect(url_for('home_page'))

    if form.errors != {}: # if validation wasn't successful, present errors
        for  msg in form.errors.values():
            flash(f'There was an error with budget registration: {msg}')
    return render_template('budget_form.html', form = form)
