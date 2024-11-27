from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *

# Define the Blueprint for 'artists'
artists_bp = Blueprint('artists', __name__, url_prefix='/artists')

# Define the route for '/artists/ppl'
@artists_bp.route('/')

def people():
    return render_template('artists/people.html')
def