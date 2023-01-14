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

class Budget(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    budget = db.Column(db.Integer(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

