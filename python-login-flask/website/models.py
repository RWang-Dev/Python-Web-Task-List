# File for creating database models for both users and the notes
from . import db    # imports db from _init_.py
from flask_login import UserMixin   # Flask handles login with this
from sqlalchemy.sql import func    # Handles the date and time for note automatically
    # Func gets the current day and time and stores it in the time when the note is created

# Database for notes, and defines what key and values are in the database
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # Primary identifier: different for each user
    data = db.Column(db.String(10000))  # Max Length of note
    date = db.Column(db.DateTime(timezone = True), default=func.now())
    # Need to set up a relationship between the note and user
    # Use foreign key: A key on a database column that references an id on another database's column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # "user.id (lowercase) references the "User" class

# Database for Users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)  # Primary identifier: different for each user
    email = db.Column(db.String(150), unique = True)    # Unique identifier: No two users can have the same email
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
