# Import necessary modules
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import appDataBase
from flask_login import login_user, login_required, logout_user, current_user

# Create a Flask Blueprint named 'auth' for authentication routes
authBP = Blueprint('auth', __name__)

# Route handler for user sign up
@authBP.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        # Retrieve form data from the request
        eMail = request.form.get('email')
        fName = request.form.get('firstName')
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password2')
        
        # Check sign up requirements
        user = User.query.filter_by(eMail=eMail).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(eMail) < 5:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(fName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif pass1 != pass2:
            flash('Passwords don\'t match.', category='error')
        elif len(pass1) < 6:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create a new User object with the form data and add it to the database
            newUser = User(eMail=eMail, fName=fName, password=generate_password_hash(pass1, method='sha256'))
            appDataBase.session.add(newUser)
            appDataBase.session.commit()
            
            # Log in the newly created user and redirect to the home page
            login_user(newUser, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    
    # Render the 'signUp.html' template and pass the current user object
    return render_template("signUp.html", user=current_user)

# Route handler for user login
@authBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data from the request
        eMail = request.form.get('email')
        pass1 = request.form.get('password')
        
        # Check if the email exists in the database
        user = User.query.filter_by(eMail=eMail).first()
        if user:
            # Check if the provided password matches the hashed password in the database
            if check_password_hash(user.password, pass1):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    
    # Render the 'login.html' template and pass the current user object
    return render_template("login.html", user=current_user)

# Route handler for user logout
@authBP.route('/logout')
@login_required
def logout():
    # Log out the current user and redirect to the login page
    logout_user()
    return redirect(url_for('auth.login'))
