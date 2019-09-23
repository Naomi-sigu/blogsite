from flask import render_template, url_for, flash, redirect
from blogsite import app, db, bcrypt
from blogsite.forms import RegistrationForm, LoginForm
from blogsite.models import User, Blog
from flask_login import login_user, logout_user



@app.route("/")
def home():
    return render_template('home.html',)
     

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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/blog/new",  methods=['GET', 'POST'])
@login_required
def new_blog():
    form = PostForm()  
    if form.validate_on_submit():
        flash('Your Post Has Been Created!', 'success')
        return redirect(url_for('home'))  
    return render_template('new_blog.html', title='New Post', f
    orm=form)