import os
from flask import Flask
from app.utils import *
from app.db.db import get_db

# Importation des blueprints de l'application
# Chaque blueprint contient des routes pour l'application
from app.views.home import home_bp
from app.views.auth import auth_bp
from app.views.artists import artists_bp
from app.views.user import user_bp
from app.views.create import create_bp
from app.views.galleries import galleries_bp
from app.views.projects import projects_bp
# Fonction automatiquement appelée par le framework Flask lors de l'exécution de la commande python -m flask run permettant de lancer le projet
# La fonction retourne une instance de l'application créée
def create_app():

    # Crée l'application Flask
    app = Flask(__name__)

    # Chargement des variables de configuration stockées dans le fichier config.py
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), "config.py"))

    # Enreigstrement des blueprints de l'application.
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(artists_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(create_bp)
    app.register_blueprint(galleries_bp)
    app.register_blueprint(projects_bp)
    
    @app.context_processor
    def inject_user():
        user = None
        if 'id_user' in session:
            db = get_db()
            user = db.execute("SELECT * FROM users WHERE id_user = ?", (session['id_user'],)).fetchone()
        return dict(user=user)
    # On retourne l'instance de l'application Flask
    return app