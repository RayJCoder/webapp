from flask import Blueprint, render_template, request, redirect, flash, jsonify, url_for, current_app
from flask_login import login_required, current_user 
from sqlalchemy import inspect
from . import db 
import json
from .models import Note, MenuCategory, Menu


# this is our blueprint, lots root and URL
views = Blueprint('views',__name__) # keep this the same as the python file for easier convention

@views.route('/', methods=['GET','POST'])
@login_required
def note():
    if request.method == 'POST':
        note = request.form.get('note')
        print(note)
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("note.html", user=current_user)    
@views.route("/about-us")
def about_us():
    return render_template("about-us.html")



@views.route('/menu')
def menu():
    menucategory = MenuCategory.query.all()
    menuitems = Menu.query.all()
    return render_template('menu.html', menucategory=menucategory,menuitems=menuitems, image_loc = current_app.config['UPLOAD_FOLDER'])


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
