from website import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from website.models import User
from website.forms import RegisterForm, LoginForm
from website import db


#-----------------HOME---------------------------#
@app.route('/')
@app.route('/home/')
def home_page():
    return render_template("home.html")


#-----------------REGISTER---------------------------#
@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    #registration validation, if successful, return to home page after
    if form.validate_on_submit():
        new_user = User(username=form.username.data, encrypt_pass = form.password.data, email_adress=form.email_address.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"You have successfully registered as {new_user.username}! Good Luck on budgeting successfully")
        #return home
        return redirect(url_for('home_page'))

    if form.errors != {}: # if validation wasn't successful, present errors
        for msg in form.errors.values():
            flash(f'There was an error with registration: {msg}')
    
    #direct user to register page
    return render_template('register.html', form=form)

#-----------------LOGIN---------------------------#
@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    #login validation, if successful, return to home page after
    if form.validate_on_submit():
        login_user = User.query.filter_by(username = form.username.data).first()
        if login_user and login_user.check_password(pass_attempt = form.password.data):
            login_user(login_user)
            flash(f'You have successfully logged in as {login_user.username}')
            return redirect(url_for('home_page'))
        else:
            flash('Sorry, the username and password does not match an account. Please try again.')
    return render_template('login.html', form = form)

#-----------------EXPENSES---------------------------#
@app.route('/expenses/', methods=['GET', 'POST'])
def submit_expenses():
    form = RegisterForm()
    #registration validation, if successful, return to home page after
    if form.validate_on_submit():
        new_user = User(username=form.username.data, encrypt_pass = form.password.data, email_adress=form.email_address.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"You have successfully registered as {new_user.username}! Good Luck on budgeting successfully")
        #return home
        return redirect(url_for('home_page'))

    if form.errors != {}: # if validation wasn't successful, present errors
        for msg in form.errors.values():
            flash(f'There was an error with registration: {msg}')
    
    #direct user to register page
    return render_template('register.html', form=form)
