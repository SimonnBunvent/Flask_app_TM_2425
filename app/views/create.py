from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from app.db.db import get_db, close_db
from app.utils import *
import os

create_bp = Blueprint('create', __name__, url_prefix='/create')


@create_bp.route('/', methods=('GET', 'POST'))
def createproject():
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        deadline = request.form['deadline']
        no_participants = request.form['no_participants']
        color = request.form['color']
        selected_format = request.form['format']
        db.execute("INSERT INTO galleries (name, description, no_participants, deadline, color, format) VALUES (?, ?, ?, ?, ?, ?)",(name, description, no_participants, deadline, color, selected_format,))
        db.commit()

        db.commit()

        close_db()
        return redirect(url_for("create.send"))

    return render_template('create/createproject.html')


@create_bp.route('/send', methods=('GET', 'POST'))
def send():
    db = get_db() 
    id_user = session.get('id_user')
    
    if not id_user:
        return redirect(url_for('auth.login'))
    
    id_gallery = db.execute("SELECT id_gallery FROM galleries ORDER BY id_gallery DESC LIMIT 1").fetchone()
    id_gallery = id_gallery['id_gallery']


    gallery = db.execute("SELECT galleries.* FROM galleries JOIN has_u_g ON galleries.id_gallery = has_u_g.FK_gallery WHERE has_u_g.FK_user = ? ORDER BY galleries.id_gallery DESC LIMIT 1", (id_user,)).fetchone()
    all_users = db.execute("SELECT username FROM users").fetchall()


    if request.method == 'POST':
        selected_users = request.form.getlist('users')

        existing_entry = db.execute(
            "SELECT 1 FROM has_u_g WHERE FK_user = ? AND FK_gallery = ?",
            (id_user, id_gallery)
        ).fetchone()
        
        if not existing_entry:
            db.execute("INSERT INTO has_u_g (FK_user, FK_gallery) VALUES (?, ?)", (id_user, id_gallery))

        for selected_user in selected_users:
            if selected_user:
                user = db.execute("SELECT id_user FROM users WHERE username = ?", (selected_user,)).fetchone()
                if user:
                    existing_entry = db.execute(
                        "SELECT 1 FROM has_u_g WHERE FK_user = ? AND FK_gallery = ?",
                        (user['id_user'], id_gallery)
                    ).fetchone()

                    if not existing_entry:
                        db.execute("INSERT INTO has_u_g (FK_user, FK_gallery) VALUES (?, ?)", (user['id_user'], id_gallery))

        db.commit()

        return redirect(url_for('projects.projects'))


    return render_template('create/send.html', all_users=all_users, no_participants=gallery['no_participants'])
