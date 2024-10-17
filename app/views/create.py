from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

create_bp = Blueprint('create', __name__)


def create_project():
    return render_template('create/createproject.html')