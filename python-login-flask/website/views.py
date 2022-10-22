# This file stores all the standard routes, which is the different pages that the user can access

from flask import Blueprint, render_template, request, flash, jsonify
    # A blueprint stores all the urls and views of the different website pages
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
    # Json is built into Python

views = Blueprint('views', __name__)    

@views.route('/', methods=['GET', 'POST'])  # Checks the URL and runs the function accordingly
@login_required # Cannot access home unless logged in
#home page decorator 
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')   
    return render_template("home.html", user=current_user)  # Flask handles rendering the HTML we wrote to the web

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # Notes are loaded as a Python dictionary
    noteId = note['noteId']
    note = Note.query.get(noteId)   # .get accesses the primary key of the field
    if note:
        if note.user_id == current_user.id: # Security check to see if the current user signed in owns the note
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

