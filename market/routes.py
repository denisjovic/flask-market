from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from market import db
from market import bcrypt
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def hello():
    return render_template('home.html')

@app.route('/market')
@login_required
def market():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'User created! Welcome {user_to_create.username}!', category='success')
        return redirect(url_for('market'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}", category='danger')
    return render_template('register.html', form=form)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash(f'Welcome {user.username.capitalize()}! You are now logged in!', category='success')
                return redirect(url_for('market'))
            flash('Wrong password!', category='danger')
            return redirect(url_for('login'))
        flash('User does not exist', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('hello'))