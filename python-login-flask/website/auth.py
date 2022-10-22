from flask import Blueprint, render_template, request, flash, redirect, url_for
    # Handles URLs and redirects
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
    # Never stores password as the password itself, but as a hash with no inverse function
from . import db
from flask_login import login_user, login_required, logout_user, current_user
    # This import manages what tabs the user can and cannot see based on whether they are logged in or out
    # Current user stores all information about the current user that is logged in

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST']) # Specifies what HTTP requests this route can accept
def login():
    if request.method == 'POST':
        # Gets the form data that we sent to the server using the Flask request import
        email = request.form.get('email')   
        password = request.form.get('password')

        # Filter all the users by email and check if this user is actually entering the right info
        user = User.query.filter_by(email = email).first()  # Finds the user by email in the database
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category = 'success')
                login_user(user, remember=True) # Remembers that the user is logged in
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category = 'error')
        else:
            flash('Email does not exist', category = 'error')

    data = request.form
    print(data)
    return render_template("login.html", user=current_user) # Renders each of the templates built off the base template in each function
        # Second parameter passes in information to the template

@auth.route('/logout')
@login_required # Does not run unless user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Stores the form information if POST request into variables
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()

        # (SECURITY CHECK) Make sure all the information passed is valid
        # Use message flashing using flask to show when information is not correct
        if user:
            flash('Email already exists.', category = 'error')  # Flash messages on the screen using Flask module
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:   # Everything is good
            new_user = User(email = email, first_name = first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)    # Important: actually adds the user and commits to the database
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created successfully!", category="success")
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)
