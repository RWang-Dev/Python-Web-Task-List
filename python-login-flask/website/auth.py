from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# This import manages what tabs the user can and cannot see based on whether they are logged in or out
from flask_login import login_user, login_required, logout_user, current_user

# A blueprint stores all the urls and views

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

# Filter all the users by email and check if this user is actually entering the right info
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category = 'success')
                # Remembers that the user is logged in
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category = 'error')
        else:
            flash('Email does not exist', category = 'error')

    # Passing values to templates in the backend ex: text
    data = request.form
    print(data)
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()

        if user:
            flash('Email already exists.', category = 'error')
# Make sure all the information passed is valid
# Use message flashing using flask to show when information is not correct
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            new_user = User(email = email, first_name = first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user) 
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created successfully!", category="success")
            return redirect(url_for('views.home'))
    return render_template("sign-up.html", user=current_user)
