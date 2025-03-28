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

@galleries_bp.route('/', methods=['GET', 'POST'])
def gallery():
    return render_template('galleries/gallery.html')