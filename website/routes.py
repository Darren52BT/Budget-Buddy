from website import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from website.models import User, Budget, Week, Expense
from website.forms import RegisterForm, LoginForm, BudgetForm, WeekForm, ExpenseListForm
from website import db
from flask_login import login_user, logout_user, login_required, current_user

#-----------------LANDING---------------------------#
@app.route('/')
def landing_page():
    return render_template("landing.html")

#-----------------HOME---------------------------#
@app.route('/home/', methods=['GET', 'POST'])
@login_required
def home_page():
    form = WeekForm()
    if request.method == "POST" and form.validate_on_submit:
        expenseForm = ExpenseListForm()
        week = Week.query.filter_by(id = request.form.get('current_week')).first()
        expenses = Expense.query.filter_by(budgetOwner_Id = week.budget.id).all()
        flash(f"You have successfully chosen {week}", category='success')
        return render_template('expense_list.html', current_week = week, current_expenses = expenses, form = expenseForm)
    else:
        flash(f'There was a problem with selecting a week', category="danger")
    return render_template("home.html", weeks = current_user.weeks, form = form)


#-----------------REGISTER---------------------------#
@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    #registration validation, if successful, return to home page after
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password = form.password.data, email_address=form.email_address.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"You have successfully registered as {new_user.username}! Good Luck on budgeting successfully", category="success")
        #return home
        return redirect(url_for('login_page'))

    if form.errors != {}: # if validation wasn't successful, present errors
        for  msg in form.errors.values():
            flash(f'There was an error with registration: {msg}', category="danger")
    
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
            flash(f'You have successfully logged in as {return_user.username}', category="success")
            return redirect(url_for('home_page'))
        else:
            flash('Sorry, the username and password does not match an account. Please try again.', category="danger")
    return render_template('login.html', form = form)


#-----------------LOGOUT ------------------------#
@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have logged out successfully. Remember to keep track of your budget!', category="info")
    return redirect(url_for('landing_page'))

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
        flash(f'You have successfully created a week {new_week.id} with a budget of{new_week.budget.budget}', category="success")
        return redirect(url_for('home_page'))

    if form.errors != {}: # if validation wasn't successful, present errors
        for  msg in form.errors.values():
            flash(f'There was an error with budget registration: {msg}', category="danger")
    return render_template('budget_form.html', form = form)

#--------------------------------EXPENSE LIST --------------#

@app.route('/week-expenses', methods=['GET', 'POST'])
@login_required
def expense_list_page():
    form = ExpenseListForm()
    if request.method == "POST":
        return render_template('expense_list.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    expense = Expense.query.filter_by(id = id).first()
    form = ExpenseListForm()
    if request.method =="POST":
        expense.cost = int(form.cost.data)
        expense.label = form.label.data
        flash(f'You have successfully updated an expense to {expense.label}: ${expense.cost}', category='success')
        return render_template("expense_list.html",form = form, current_week = Week.query.filter_by(budget = Budget.query.filter_by(id = expense.budgetOwner_Id).first()).first())
    else:
        flash("You have failed to update a task", category='danger')
    return render_template("expense_list.html",form = form, current_week = Week.query.filter_by(budget = Budget.query.filter_by(id = expense.budgetOwner_Id).first()).first())
