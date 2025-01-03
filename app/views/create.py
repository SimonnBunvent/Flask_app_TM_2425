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
        db = get_db()


        if name and no_participants:
            db.execute("INSERT INTO galleries (name, description, no_participants, deadline) VALUES (?, ?, ?, ?)",(name, description, no_participants, deadline))
            db.commit()
            close_db()
            
            return redirect(url_for("create.send"))
    else:
        return render_template('create/createproject.html')   
            


@create_bp.route('/send')
def send():
    return render_template('create/send.html')