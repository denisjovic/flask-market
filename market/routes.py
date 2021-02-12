from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from market import bcrypt
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def hello():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == 'POST':

        # Buying Items
        purchased_item = request.form.get('purchased_item')
        purchased_item_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_item_object:
            if current_user.can_purchase(purchased_item_object):
                purchased_item_object.buy(current_user)
                flash(f"You have bought {purchased_item_object.name}!", category="success")
            else:
                flash(f"Unfortunately, you don't have enough money to buy {purchased_item_object.name}!",
                      category="danger")
        #Selling Items
        sold_item = request.form.get('sold_item')
        sold_item_object = Item.query.filter_by(name=sold_item).first()
        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                sold_item_object.sell(current_user)
                flash(f"You have sold {sold_item_object.name}!", category="success")
            else:
                flash("Something went wrong, item was not sold!", category="danger")               
        return redirect(url_for('market'))

    else:

        # Show only items that no one has bought
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, 
                                purchase_form=purchase_form, 
                                owned_items=owned_items,
                                selling_form=selling_form
                                )



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
