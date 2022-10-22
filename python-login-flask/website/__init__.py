from flask import Flask
from flask_sqlalchemy import SQLAlchemy    # Using this for the database
from os import path
from flask_login import LoginManager
# When __init__ is put inside a folder, the folder becomes a package when imported

db = SQLAlchemy()   # Creates the database for us
DB_NAME = "database.db"

# Initializes the app using Flask 
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Random-string"  #encrypts the data for this app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # f'sqlite stores the database in this folder
    db.init_app(app)    # Takes the database and tells it that this is the app that is associated with it
 
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

    # Sepcifies what page the user should be on if they are not logged in
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader  # Telling Flask how we load a user. 
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    # Checks if a database already exists, if not, create one
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")


