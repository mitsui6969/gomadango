from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import validators
from itsdangerous.url_safe import URLSafetimedSerializer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

@app.route('/setting', method=['GET', 'POST'])
def setting_home():
    setting =  user.query.all()
    return render_template('index.html')

@app.route('/setting/pass/mail', method=['GET', 'POST'])
def pas_change():
    if request.method == 'POST':
        pas = request.form['pas']
        new_pas = request.form['new_pas']
        user = User.query.filter_by(email=email, password=password).first()
        db.session.delete(pas)
        db.session.add(new_pas)
        db.session.commit()
        if user:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')
    