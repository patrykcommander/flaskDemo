from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required




posts = [
    {

        'title': 'Blog post 1',
        'content':'Test content 1',
        'author':'Patryk O',
        'date_posted': datetime.now().strftime("%d/%m/%Y")

    } , {

        'title': 'Blog post 2',
        'content':'Test content 2',
        'author':'John Dere',
        'date_posted': datetime.now().strftime("%d/%m/%Y")
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    formReg = RegistrationForm()
    if formReg.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(formReg.password.data).decode('utf-8') 
        # hashing the password entered by the user
        # decode function returns the hased password as a string (else without the decode func, the has function returns the byte version)
        user = User(userName = formReg.userName.data, email = formReg.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {formReg.userName.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=formReg)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    formLog = LoginForm()
    if formLog.validate_on_submit():
        user = User.query.filter_by(email=formLog.email.data).first()
        if user and bcrypt.check_password_hash(user.password , formLog.password.data):
            login_user(user, remember=formLog.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('account')) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=formLog)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

