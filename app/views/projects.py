from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from app.db.db import get_db, close_db
from app.utils import *
import os
from werkzeug.utils import secure_filename

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'app/static/imgs/oeuvres/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@projects_bp.route('/', methods=['GET','POST'])
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
    
    images = {}
    for gallery in galleries:
        id_gallery = gallery["id_gallery"]
        gallery_images = db.execute(
            """
            SELECT images.* 
            FROM images 
            INNER JOIN contains ON images.id_img = contains.FK_img 
            WHERE contains.FK_gallery = ?
            """,
            (id_gallery,)
        ).fetchall()
        images[id_gallery] = gallery_images

    if request.method == 'POST' and 'publish' in request.form:
        id_gallery = request.form.get('id_gallery')
        if id_gallery:
            db.execute("UPDATE galleries SET published = ? WHERE id_gallery = ?", (1, id_gallery))
            db.commit()

    close_db()
    return render_template('projects/projects.html', galleries=galleries, images=images)

@projects_bp.route('/<int:id_gallery>/<name>', methods=('GET', 'POST'))
def project(id_gallery, name):
    db = get_db()
    id_user = session.get('id_user')
    gallery = db.execute("SELECT * FROM galleries WHERE id_gallery = ? AND name = ?", (id_gallery, name)).fetchone()
    no_users = gallery['no_participants']
    participants = db.execute("SELECT users.* FROM users JOIN has_u_g ON users.id_user = has_u_g.FK_user WHERE has_u_g.FK_gallery = ?", (id_gallery,)).fetchall()
    images = {p["id_user"]: db.execute("""SELECT * FROM images JOIN has_u_i ON images.id_img = has_u_i.FK_img WHERE has_u_i.FK_user = ? AND images.id_img IN (SELECT FK_img FROM contains WHERE FK_gallery = ?)""", (p["id_user"], id_gallery)).fetchone()for p in participants}
    img_format = gallery['format']
    image_count = db.execute("SELECT COUNT(*) FROM contains WHERE FK_gallery = ?", (id_gallery,)).fetchone()[0]
    user_image = db.execute("SELECT images.* FROM images JOIN has_u_i ON images.id_img = has_u_i.FK_img JOIN contains ON images.id_img = contains.FK_img WHERE has_u_i.FK_user = ? AND contains.FK_gallery = ?",(id_user, id_gallery)).fetchone()

    no_images = image_count == 0
    latest_image = None if no_images else db.execute(
        "SELECT * FROM images JOIN contains ON images.id_img = contains.FK_img WHERE contains.FK_gallery = ? ORDER BY images.id_img DESC LIMIT 1",
        (id_gallery,)
    ).fetchone()

    if request.method == 'POST':
        project_name = request.form.get('project_name', '').strip()
        description = request.form.get('img_desc', '').strip()
        img = request.files.get('img')

        if img and img.filename and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            img.save(save_path)

            file_path = os.path.join('imgs', 'oeuvres', filename).replace("\\", "/")

            db.execute(
                "INSERT INTO images (users, description, project_name, date, path_to_file, format) VALUES (?, ?, ?, CURRENT_DATE, ?, ?)",
                (no_users, description, project_name, file_path, img_format)
            )

            id_img = db.execute("SELECT id_img FROM images ORDER BY id_img DESC LIMIT 1").fetchone()

            if id_img:
                db.execute("INSERT INTO contains (FK_img, FK_gallery) VALUES (?, ?)", (id_img[0], id_gallery))
                db.execute("INSERT INTO has_u_i (FK_img, FK_user) VALUES (?, ?)", (id_img[0], id_user))

        db.commit()
        close_db()

        return redirect(url_for("projects.project", id_gallery=id_gallery, name=name))  

    return render_template("projects/project.html", gallery=gallery, image=latest_image, images=images, participants=participants, user_image=user_image)