from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db, close_db
import os

create_bp = Blueprint('create', __name__, url_prefix='/create')

@create_bp.route('/createproject')
def createproject():
    return render_template('create/createproject.html')