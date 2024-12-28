from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *


create_bp = Blueprint('create', __name__, url_prefix='/create')

@create_bp.route('/', methods=('GET', 'POST'))
def createproject():
    return render_template('create/createproject.html')


@create_bp.route('/send')
def send():
    return render_template('create/send.html')