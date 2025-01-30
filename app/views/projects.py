from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from app.db.db import get_db, close_db
from app.utils import *
import os

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/')
def projects():
    id_user = session.get('id_user')
    if not id_user:
        return "Error: User not logged in.", 400

    db = get_db()

    # Count galleries for the user
    result = db.execute(
        "SELECT COUNT(*) AS gallery_count FROM has_u_g WHERE FK_user = ?", 
        (id_user,)
    ).fetchone()
    gallery_count = result['gallery_count'] if result else 0

    # Get gallery details if needed
    galleries = db.execute(
            """
            SELECT galleries.*
            FROM galleries
            INNER JOIN has_u_g ON galleries.id_gallery = has_u_g.FK_gallery
            WHERE has_u_g.FK_user = ?

            """, 
            (id_user,)
        ).fetchall()
    # Debugging info
    print(f"User {id_user} owns {gallery_count} galleries.")
    print(f"Galleries: {galleries}")

    # Render template
    if gallery_count == 0:
        return render_template('user_galleries.html', messages=[])

    # "Hello world!" messages or gallery names
    messages = [f"Gallery: {gallery['name']}" for gallery in galleries]
    close_db()
    return render_template('projects/projects.html', galleries=galleries)

@projects_bp.route('/project1')
def project():
    return render_template('projects/project.html')

    