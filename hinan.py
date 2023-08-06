from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stu_num = db.Column(db.Integer)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    user_reserve = db.relationship('User', backref='user')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        stu_num = request.form['stu_num']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(stu_num=stu_num).first()
        if user is None:
            user = User(stu_num=stu_num, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ###予約履歴###
@app.route('/post/history', methods=['GET', 'POST'])
@login_required #予約履歴だから予約のコード見て変える
def history_post():
    if request.method == 'POST':
        #　↓　予約のみて変える
        post = Post(timestamp=datetime.now(pytz.timezone('Asia/Tokyo')))
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('history.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)