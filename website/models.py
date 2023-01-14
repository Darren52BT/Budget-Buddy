from website import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length = 25), nullable = False, unique = True)
    encrypt_pass = db.Column(db.String(length=100), nullable=False)
    email_address = db.Column(db.String(length=50), nullable = False, unique = True)
    weeks = db.relationship('Week', backref='user', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, text_pass):
        self.encrypt_pass = bcrypt.generate_password_hash(text_pass).decode('utf-8')
    
    def check_password(self, pass_attempt):
        return bcrypt.check_password_hash(self.encrypt_pass, pass_attempt)
    def __repr__(self):
        return f'User %s' % self.username


class Week(db.Model):
    id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    budget = db.relationship('Budget', backref='user', uselist=False, lazy=True)
    def __repr__(self):
            return f'Week {self.id}'

class Budget(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    weekOwner_Id = db.Column(db.Integer(), db.ForeignKey('week.id'))
    budget = db.Column(db.Integer(), nullable = False)
    budgetLeft = db.Column(db.Integer(), nullable=False)
    expenses = db.relationship('Expense', backref='user', uselist=False, lazy=True)

    def __repr__(self):
        return f'Budget %s' % self.budget

class Expense(db.Model):
    id = db.Column(db.Integer(), primary_key =True)
    label = db.Column(db.String(length = 30), nullable = False)
    cost = db.Column(db.Integer(), nullable = False)
    budgetOwner_Id = db.Column(db.Integer(), db.ForeignKey('budget.id'))
    
    def __repr__(self):
        return f'Expense %s' % self.label
    
