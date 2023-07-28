# Import necessary modules
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import appDataBase
import json

views = Blueprint('views', __name__)    # Create a Flask Blueprint named 'views'

# Route handler for the root URL ('/') - requires login
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Retrieve the note from the HTML form
        note = request.form.get('note')
        
        if len(note) < 1:
            # Validate note length and flash an error message if it's too short
            flash('Notes must be longer', category='error')
        else:
            # Create a new Note object with the note and current user ID
            new_note = Note(noteText=note, userId=current_user.id)
            # Add the new note to the database
            appDataBase.session.add(new_note)
            appDataBase.session.commit()
            # Flash a success message
            flash('Note added successfully!', category='success')

    # Render the 'home.html' template and pass the current user object
    return render_template("home.html", user=current_user)

# Route handler for deleting a note
@views.route('/deleteNote', methods=['POST'])
def delete_note():
    # Parse the JSON payload from the request
    pesonalNote = json.loads(request.data)
    # Retrieve the note ID from the payload
    id = pesonalNote['id']
    # Query the Note table using the ID
    pesonalNote = Note.query.get(id)
    
    if pesonalNote:
        if pesonalNote.userId == current_user.id:
            # Delete the note if it exists and belongs to the current user
            appDataBase.session.delete(pesonalNote)
            appDataBase.session.commit()

    # Return an empty JSON response
    return jsonify({})