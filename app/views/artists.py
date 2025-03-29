from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db, close_db
from app.utils import *

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
    return render_template('artists/user_profile.html', user=user)
