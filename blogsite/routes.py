from flask import render_template, url_for, flash, redirect
from pitcharea import app, db, bcrypt
from pitcharea.forms import RegistrationForm, LoginForm
from pitcharea.models import User, Pitch
from flask_login import login_user


posts = [
    {
        'Author': 'nammy',
        'Title': 'Pitch Post',
        'Content': 'First pitch made',
        'Date_posted': 'April 20, 2018'
    },
    {
        'Author': 'Jane Doe',
        'Title':  'save Post',
        'Content': 'Second Blog Post',
        'Date_posted': 'April 20, 2018'
    }

]

@app.route("/")
def home():
    return render_template('home.html', posts = posts)
     

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account Has Been Created You Can Now LogIn', "success")
        return redirect(url_for("login"))
    return render_template('register.html', title = 'Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:    
            flash('Login Unsuccessful. Please check your email or password to try again.', 'danger')
    return render_template('login.html', title = 'Login', form=form)    

