from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db, close_db
from app.utils import *
import os

artists_bp = Blueprint('artists', __name__, url_prefix='/artists')

@artists_bp.route('/')

def people():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()

    if g.user:
        users = [user for user in users if user["username"] != g.user["username"]]

    return render_template('artists/people.html', users=users)

@artists_bp.route('/<username>', methods=('GET', 'POST'))

def user_profile(username):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    id_user = db.execute("SELECT id_user FROM users WHERE username = ?", (username,)).fetchone()
    id_user = id_user["id_user"] if id_user else None

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

    return render_template('artists/user_profile.html', user=user, galleries=galleries, images=images, artists=artists)
