from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# Database initialise
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    boostrap = Bootstrap(app)

    app.secret_key = 'somerandomvalue'

    # DatabaseConfig
    # app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///travel123.sqlite'
    # db.init_app(app)

    # ImageUploadPat
    # UPLOAD_FOLDER = '/static/image'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import events
    app.register_blueprint(events.eventbp)

    return app
