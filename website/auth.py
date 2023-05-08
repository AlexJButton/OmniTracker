from flask import Blueprint, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/OmniLogin')
def login():
    return render_template("OmniLogin.html")


@auth.route('/OmniLogin', methods=["POST"])
def login2():
    # Getting the for responses
    email = request.form.get("email")
    password = request.form.get("password")
    rememberMe = True if request.form.get("remember") else False

    # getting the user by its email if it exists
    checkUsr = User.query.filter_by(email=email).first()

    if not checkUsr or not check_password_hash(checkUsr.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    # Going to the main page because the email and password must be correct to reach here
    login_user(checkUsr, remember=rememberMe)
    return redirect(url_for('views.home'))


@auth.route('/OmniSignUp')
def signup():
    return render_template("OmniSignUp.html")


@auth.route('/OmniSignUp', methods=["POST"])
def signup2():
    # Getting the for responses
    email = request.form.get("email")
    password = request.form.get("password")

    # Checking if the user email already exists
    checkUsr = User.query.filter_by(email=email).first()
    if checkUsr:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # Creating the User, hashes the password for security
    newUser = User(email=email, password=generate_password_hash(password, method='sha256'))

    # Adding the User to the db
    db.session.add(newUser)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/OmniLogout')
@login_required
def logout():
    uID = current_user.id
    user = User.query.get(int(uID))

    return render_template("OmniLogout.html", email=user.email)

@auth.route('/OmniLogout', methods=["POST"])
@login_required
def logout2():
    if request.method == "POST":
        logout_user()
    return redirect(url_for('views.home'))