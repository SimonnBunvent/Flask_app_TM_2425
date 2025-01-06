from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
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
        db = get_db()


        if name and description and deadline and no_participants:
            db.execute("INSERT INTO galleries (name, description, no_participants, deadline, color) VALUES (?, ?, ?, ?, ?)",(name, description, no_participants, deadline, color))
            db.commit()
            close_db()
            return redirect(url_for("create.send"))

    else:
        return render_template('create/createproject.html')   
    
def user_gallery():
    if request.method =='GET':

        username = request.args('username')
        name = request.args('name')

        db = get_db()

        query = '''
        SELECT g.*
        FROM galleries g
        JOIN has_u_g ON g.id = ug.FK_gallery
        JOIN users u ON u.id = ug.FK_user
        WHERE u.username = ? AND g.name = ?
        '''
        gallery = db.execute(query, (name, username)).fetchone()
        close_db()
        if gallery:
            return{'gallery': dict(gallery)}, 200
        else:
            return {'error': 'No gallery found for this user'}, 404
        

@create_bp.route('/send', methods=('GET', 'POST'))
def send():
    if request.method == 'POST':

        id_gallery = request.form['id_gallery']

        db = get_db()

        gallery = db.execute('SELECT * FROM galleries WHERE id_gallery =?', (id_gallery,)).fetchone()
        close_db()

        if gallery:
            gallery_id = gallery[1]
            return f"YESYESYES"
        else:
            return f"NONONO"
    else:
        return render_template('create/send.html')  
