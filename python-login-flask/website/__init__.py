from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Random-string"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # Takes the database and tells it that this is the app that is associated with it

    
    # tell flask that we have blueprints aka views
    from .views import views
    from .auth import auth



    # / essentially means no prefix, empty string
    # ''' The url_prefix is what has to be the prefix
    # of the url sepcified in the views.py and auth.py file,
    # so typically set as nothing, or / '''
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        


    return app


def create_database(app):
    # Checks if a database already exists, if not, create one
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")


