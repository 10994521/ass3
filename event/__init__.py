from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Database initialise
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    boostrap = Bootstrap(app)

    app.secret_key = 'somerandomvalue'

    # Configue and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seminar.sqlite'
    db.init_app(app)

    # initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ImageUploadPat
    # UPLOAD_FOLDER = '/static/image'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Blueprints
    from . import views
    app.register_blueprint(views.mainbp)

    from . import manage
    app.register_blueprint(manage.managebp)

    from . import details
    app.register_blueprint(details.detailsbp)

    from . import profile
    app.register_blueprint(profile.profilebp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
