from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db, close_db
import os

gallery_bp = Blueprint('gallery', __name__,url_prefix='/gallery')

@gallery_bp.route('/artworks')
def artworks():
    return render_template('artworks.html')