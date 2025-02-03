from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from app.db.db import get_db, close_db
from app.utils import *
import os

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

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

@projects_bp.route('/project1')
def project():
    return render_template('projects/project.html')

    