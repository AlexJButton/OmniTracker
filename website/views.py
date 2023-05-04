from flask import Blueprint, render_template, request, Flask
from flask_login import login_required, current_user
from. import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("OmniHome.html")


@views.route('/OmniView')
@login_required
def view():
    return render_template("OmniView.html")


@views.route('/OmniMake')
@login_required
def make():
    return render_template("OmniMake.html")


@views.route('/OmniCalendar')
@login_required
def calendar():
    return render_template("OmniCalendar.html")
