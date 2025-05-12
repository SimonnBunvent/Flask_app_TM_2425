from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from app.db.db import get_db, close_db
import os
from werkzeug.utils import secure_filename

user_bp = Blueprint('user', __name__, url_prefix='/user')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'app/static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required 
def show_profile():
    id_user = session.get('id_user')
    db = get_db()
    
    user = db.execute("SELECT * FROM users WHERE id_user = ?", (id_user,)).fetchone()

    galleries = db.execute(
        """
        SELECT galleries.* 
        FROM galleries 
        JOIN has_u_g ON galleries.id_gallery = has_u_g.FK_gallery 
        WHERE has_u_g.FK_user = ?
        """, 
        (id_user,)
    ).fetchall()

    artists_by_gallery = {}
    artists = []

    for gallery in galleries:
        id_gallery = gallery["id_gallery"] 

        artists = db.execute(
            """
            SELECT users.* 
            FROM users 
            JOIN has_u_g ON users.id_user = has_u_g.FK_user 
            WHERE has_u_g.FK_gallery = ?
            """, 
            (id_gallery,)
        ).fetchall()

        artists_by_gallery[id_gallery] = artists

    images = db.execute(
        """
        SELECT images.*, galleries.name AS gallery_name 
        FROM images 
        JOIN contains ON images.id_img = contains.FK_img 
        JOIN galleries ON contains.FK_gallery = galleries.id_gallery 
        JOIN has_u_i ON images.id_img = has_u_i.FK_img 
        WHERE has_u_i.FK_user = ?
        ORDER BY images.id_img DESC
        """,
        (id_user,)
    ).fetchall()

    image = images[0] if images else None 

    return render_template('user/profile.html', user=user, galleries=galleries, images=images, image=image, artists=artists)

@user_bp.route('/edit', methods=('GET', 'POST'))
@login_required
def edit_profile():
    id_user = session.get('id_user')
    db = get_db()

    user = db.execute("SELECT profile_pic FROM users WHERE id_user = ?", (id_user,)).fetchone()
    file_path = user['profile_pic'] if user and user['profile_pic'] else None

    if request.method == 'POST':
        last_name = request.form['last_name']
        name = request.form['name']
        fav_style = request.form['fav_style']
        mini_desc = request.form['mini_desc']
        desc = request.form['desc']

        profile_pic = request.files.get('profile_pic')

        if profile_pic and profile_pic.filename and allowed_file(profile_pic.filename):
            filename = secure_filename(profile_pic.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename) 
            profile_pic.save(save_path)

            file_path = os.path.join('uploads', filename).replace("\\", "/")
            db.execute("UPDATE users SET profile_pic = ? WHERE id_user = ?",(file_path, id_user))

        db.execute("UPDATE users SET last_name = ?, name = ?, fav_style = ?, mini_desc = ?, desc = ? WHERE id_user = ?",
                    (last_name, name, fav_style, mini_desc, desc, id_user))

        db.commit()
        close_db()

        return redirect(url_for("user.edit_profile"))

    user = db.execute("SELECT * FROM users WHERE id_user = ?", (id_user,)).fetchone()
    return render_template('user/edit.html', user=user)