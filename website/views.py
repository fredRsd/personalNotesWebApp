from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import dataBase
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note') #Get Note

        if len(note) < 1:
            flash('Note is too short!', category='error') #error message: short note
        else:
            new_note = Note(text=note, user_id=current_user.id)  # note's schema
            dataBase.session.add(new_note) #note added to database 
            dataBase.session.commit() #database session commits
            flash('Note added!', category='success')    #success message

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            dataBase.session.delete(note)
            dataBase.session.commit()

    return jsonify({})
