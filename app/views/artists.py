from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db, close_db
from app.utils import *

artists_bp = Blueprint('artists', __name__, url_prefix='/artists')

@artists_bp.route('/')

def people():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    return render_template('artists/people.html', users=users)