from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from app.db.db import get_db, close_db
import os

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required
@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required 
def show_profile():
    # Affichage de la page principale de l'application
    return render_template('user/profile.html')

@user_bp.route('/edit', methods=('GET', 'POST'))
@login_required 
def edit_profile():

    id_user = session.get('id_user')

    if request.method == 'POST':
        fav_style = request.form['fav_style']
        mini_desc = request.form['mini_desc']
        desc = request.form['desc']

        db = get_db()

        if fav_style or mini_desc or desc:
            db.execute("""
                UPDATE users 
                SET 
                    fav_style = COALESCE(?, fav_style), 
                    mini_desc = COALESCE(?, mini_desc), 
                    desc = COALESCE(?, desc)
                WHERE id_user = ?
            """, (fav_style, mini_desc, desc, id_user))
            
            if g.user['fav_style'] is None:
                db.execute("INSERT INTO users (fav_style) VALUES(?)", (fav_style))
            if g.user['mini_desc'] is None:
                db.execute("INSERT INTO users (mini_desc) VALUES(?)", (mini_desc))
            if  g.user['desc'] is None:
                db.execute("INSERT INTO users (desc) VALUES(?)", (desc))
            db.commit()
            close_db()
            return redirect(url_for("user.edit"))
    else:
        return render_template('user/edit.html')
