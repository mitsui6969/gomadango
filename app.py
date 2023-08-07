from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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
    #stu_num = relationship("List", backref="user" )
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

class List(UserMixin, db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stu_num = db.Column(db.Integer)
    day = db.Column(db.Text())
    time = db.Column(db.Text())
    seat = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Tokyo')))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

###アカウント新規作成###
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        stu_num = request.form.get('stu_num')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user: # メールがすでに登録されてたらコメント出す処理
            flash('このメールアドレスはすでに登録されています')
            return redirect(url_for('register'))
        
        new_user = User(stu_num=stu_num, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
        # else: # if a user is found, we want to redirect back to signup page so user can try again
        #     flash('Email address already exists')
        #     return redirect(url_for('register'))
    return render_template('register.html')

###ログイン画面###
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email, password=password).first()
        ##メールとパスが一致しなかったらコメント出す処理
        if not user or not User.query.filter_by(email=email).first():
            flash('ログイン情報が一致しません。もう一度お試しください')
            return redirect(url_for('login'))
        ##一致したらホームに飛ばす処理
        elif user:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

###ログアウト###
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

###ホーム###
@app.route('/')
def index():
    lists = List.query.all()
    return render_template('index.html', lists = lists)

###予約画面###
@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        list = List()
    #   list.studentnumber = request.form["studentnumber"]
        list.stu_num = request.form["stu_num"]
        list.day = request.form["day"]
        list.time = request.form["time"]
        list.seat = request.form["seat"]
        list.timestamp = datetime.now(pytz.timezone('Asia/Tokyo'))
        db.session.add(list)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new.html')


###履歴画面###
@app.route('/post/history', methods=["GET", "POST"])
@login_required 
def history_post():
    if request.method == "POST":
        stu_num = request.form["stu_num"] #学籍番号入力
        matching_records = List.query.filter_by(stu_num=stu_num).all()
        return render_template('history.html', records=matching_records)
    return render_template('history.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)