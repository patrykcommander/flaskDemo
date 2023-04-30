from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'author': 'Patryk O',
        'title': 'Test Post 1',
        'content': 'Test post content',
        'date_posted': datetime(2018,12,2).strftime("%d/%m/%Y")
    },
    {
        'author': 'Patryk O',
        'title': 'Test Post 2',
        'content': 'Second post content',
        'date_posted': datetime(2022,4,14).strftime("%d/%m/%Y")
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


if __name__ == '__main__':
    app.run(debug=True)
