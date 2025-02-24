from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from app.db.db import get_db, close_db
import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')


UPLOAD_FOLDER = 'app/static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required 
def show_profile():
    id_user = session.get('id_user')
    db = get_db()
    # Affichage de la page principale de l'application
    user = db.execute("SELECT * FROM users WHERE id_user = ?", (id_user,)).fetchone()
    return render_template('user/profile.html', user=user)

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

        db.execute("UPDATE users SET last_name = ?, name = ?, fav_style = ?, mini_desc = ?, desc = ?, profile_pic = ? WHERE id_user = ?",
                    (last_name, name, fav_style, mini_desc, desc, file_path, id_user))

        db.commit()
        close_db()

        return redirect(url_for("user.edit_profile"))

    user = db.execute("SELECT * FROM users WHERE id_user = ?", (id_user,)).fetchone()
    return render_template('user/edit.html', user=user)