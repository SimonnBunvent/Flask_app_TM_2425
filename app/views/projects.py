from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *


projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/')
def projects():
    return render_template('projects/projects.html')

@projects_bp.route('/project1')
def project():
    return render_template('projects/project.html')

