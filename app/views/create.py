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
        db = get_db()


        if name and description and deadline and no_participants and color:
            db.execute("INSERT INTO galleries (name, description, no_participants, deadline, color) VALUES (?, ?, ?, ?, ?)",(name, description, no_participants, deadline, color))
            db.commit()
            close_db()
            return redirect(url_for("create.send"))

    else:
        return render_template('create/createproject.html')   
    

    
        
@create_bp.route('/send', methods=('GET', 'POST'))
def send():
    return render_template('create/send.html')

def user_gallery():
    id_user = session.get('id_user')
    id_gallery = request.form.get('id_gallery')

    db = get_db()

    db.execute("INSERT INTO has_u_g (id_user, id_gallery) VALUES (?, ?)",(id_user, id_gallery))
    db.commit()
    
