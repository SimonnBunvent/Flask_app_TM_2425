from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *

gallery_bp = Blueprint('gallery', __name__,url_prefix='/gallery')

@gallery_bp.route('/')
def artworks():
    return render_template('gallery/artworks.html')