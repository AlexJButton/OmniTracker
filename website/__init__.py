from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'OmniTracker'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Making the db with the appropriate details
    db.init_app(app)
    from . import models
    with app.app_context():
        db.create_all()

    # Setting how the user login will be tracked
    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app


