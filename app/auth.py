from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from app.forms import LoginForm, RegisterForm

# Authentication Blueprint
auth = Blueprint('auth', __name__)

# Login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'green')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'red')

    

    return render_template('auth/login.html', form=form)

# Logout Route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'green')
    return redirect(url_for('auth.login'))

# Register Route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'green')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

# Unauthorized Handler
@auth.app_errorhandler(401)
def unauthorized(error):
    flash('You need to log in to access this page.', 'yellow')
    return redirect(url_for('auth.login'))
