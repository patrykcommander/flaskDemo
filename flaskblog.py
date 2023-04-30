from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# once we want to create the DataBase, command app.app_context().push() has to be run just before the db.create_all() command
# same when we want to add a new record into the db
# db.session.add() -> function to add a record to the database
# db.session.commit() -> commits the changes made with the .add() function to the database
# User.query.all() -> returns back all of the users
# User.query.first() -> returns the first user back
# User.query.filter_by(userName='Patryk').all() -> returns back the list of all of the users, but in this app the username is unique
# User.query.filter_by(userName='Patryk').first() 
# User.query.get(primary_key) -> legacy function (still possible to use), exchanged by the db.session.get(User, primary_key)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.userName}, {self.email}, {self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}, {self.date_posted}')"



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
