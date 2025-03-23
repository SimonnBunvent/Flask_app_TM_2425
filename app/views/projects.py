from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from app.db.db import get_db, close_db
from app.utils import *
import os
from werkzeug.utils import secure_filename

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'app/static/oeuvres/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@projects_bp.route('/')
def projects():
    id_user = session.get('id_user')
    db = get_db()

    galleries = db.execute(
            """
            SELECT galleries.*
            FROM galleries
            INNER JOIN has_u_g ON galleries.id_gallery = has_u_g.FK_gallery
            WHERE has_u_g.FK_user = ?

            """, 
            (id_user,)
        ).fetchall()

    close_db()
    return render_template('projects/projects.html', galleries=galleries)

@projects_bp.route('/<int:id_gallery>/<name>', methods=('GET', 'POST'))
def project(id_gallery, name):
    id_user = session.get('id_user')
    db = get_db()
    gallery = db.execute("SELECT * FROM galleries WHERE id_gallery =? AND name = ?", (id_gallery, name)).fetchone()
    if request.method == 'POST':
        description = request.form['description']
        project_name = request.form['project_name']
        img = request.files.get('img')
        img_format = gallery['format']
        users = gallery['no_participants']
        if img and img.filename and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename) 
            img.save(save_path)

            file_path = os.path.join('uploads', filename).replace("\\", "/")
            db.execute("UPDATE images SET path_to_file = ? WHERE id_image = ?",(file_path))
        
        db.execute("UPDATE images SET project_name = ?, description WHERE id_image = ?",
                    (project_name, description))
        db.execute("INSERT INTO images (users, format, date) VALUES (?, ?, CURRENT_DATE)", (users, img_format))
    return render_template('projects/project.html', gallery=gallery)