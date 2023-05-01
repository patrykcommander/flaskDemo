from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from datetime import datetime




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
    formReg = RegistrationForm()
    if formReg.validate_on_submit():
        flash(f'Account created for {formReg.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=formReg)


@app.route("/login", methods=['GET', 'POST'])
def login():
    formLog = LoginForm()
    if formLog.validate_on_submit():
        if formLog.email.data == 'admin@blog.com' and formLog.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=formLog)