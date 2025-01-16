from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from app.db.db import get_db, close_db
from app.utils import *
import os

create_bp = Blueprint('create', __name__, url_prefix='/create')


@create_bp.route('/', methods=('GET', 'POST'))
def createproject():

     
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        deadline = request.form['deadline']
        no_participants = request.form['no_participants']
        color = request.form['color']
        id_user = session.get('id_user')
        db = get_db()

        db.execute("INSERT INTO galleries (name, description, no_participants, deadline, color) VALUES (?, ?, ?, ?, ?)",(name, description, no_participants, deadline, color))
        db.commit()

        user_gallery()

        close_db()
        return redirect(url_for("create.send"))

    return render_template('create/createproject.html')


@create_bp.route('/send', methods=('GET', 'POST'))
def send(): 
    id_user = session.get('id_user')

    db = get_db()
    g.gallery = db.execute("SELECT galleries.* FROM galleries JOIN has_u_g ON galleries.id_gallery = has_u_g.FK_gallery WHERE has_u_g.FK_user = ? ORDER BY galleries.id_gallery DESC LIMIT 1", (id_user,)).fetchone()
    db.commit()
    close_db()

    if g.gallery is None:
        flash("No gallery found for this user.", "error")
        return redirect(url_for('create.createproject'))

    return render_template('create/send.html')  

@create_bp.route('/delete_last_gallery', methods=('GET', 'POST'))
def delete_last_gallery():
    id_user = session.get('id_user')

    if not id_user:
        flash("You must be logged in to delete a gallery.", "error")
        return redirect(url_for('create.createproject'))

    db = get_db()
    id_gallery = db.execute("SELECT id_gallery FROM galleries ORDER BY id_gallery DESC LIMIT 1").fetchone()

    if id_gallery:
        id_gallery = id_gallery[0]
        db.execute("DELETE FROM galleries WHERE id_gallery = ?", (id_gallery,))
        db.commit()

    return redirect(url_for('create.createproject'))

def user_gallery():
    id_user = session.get('id_user')

    db = get_db()
    id_gallery = db.execute("SELECT id_gallery FROM galleries ORDER BY id_gallery DESC LIMIT 1").fetchone()

    if id_gallery:
        id_gallery = id_gallery[0]
    else:
        flash("No gallery found", "error")
        return redirect(url_for("create.createproject"))
    
    db.execute("INSERT INTO has_u_g (FK_user, FK_gallery) VALUES (?, ?)", (id_user, id_gallery))
    db.commit()
    return redirect(url_for("create.send"))

