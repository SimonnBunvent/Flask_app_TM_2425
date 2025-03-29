from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from app.db.db import get_db, close_db
from app.utils import *
import os

galleries_bp = Blueprint('galleries', __name__,url_prefix='/galleries')

@galleries_bp.route('/', methods=['GET', 'POST'])
def artworks():
    db = get_db()
    galleries = db.execute("SELECT * FROM galleries WHERE published = ?", ('1')).fetchall()
    
    images = {}
    for gallery in galleries:
        id_gallery = gallery["id_gallery"]

        image = db.execute("""
            SELECT * FROM images 
            JOIN contains ON images.id_img = contains.FK_img 
            WHERE contains.FK_gallery = ? 
            ORDER BY images.id_img DESC 
            LIMIT 1
        """, (id_gallery,)).fetchone()
        images[id_gallery] = image

    return render_template('galleries/artworks.html', galleries=galleries, images=images)

@galleries_bp.route('/gallery/<int:id_gallery>/<name>', methods=('GET', 'POST'))
def gallery(id_gallery, name):
    db = get_db()
    gallery = db.execute("SELECT * FROM galleries WHERE id_gallery = ? AND name = ?", (id_gallery, name)).fetchone()
    images = db.execute(
        """
        SELECT images.* 
        FROM images 
        JOIN contains ON images.id_img = contains.FK_img 
        WHERE contains.FK_gallery = ? 
        ORDER BY images.id_img DESC
        """, 
        (id_gallery,)
    ).fetchall()

    id_img = db.execute("SELECT id_img FROM images ORDER BY id_img DESC LIMIT 1").fetchone()
    id_img = id_img[0]
    
    users = db.execute(
        """
        SELECT users.* 
        FROM users 
        JOIN has_u_i ON users.id_user = has_u_i.FK_user
        WHERE has_u_i.FK_img = ? 
        ORDER BY users.id_user DESC
        """, 
        (id_img,)
    ).fetchall

    return render_template("galleries/gallery.html", gallery=gallery, images=images, users=users)