from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from config import Config

# Inicjalizacja rozszerzeń (bez aplikacji)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    # Załaduj konfigurację z config.py (Config ładuje też .env przez dotenv)
    app.config.from_object(Config)

    # Inicjalizuj rozszerzenia
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Flask-Login: ustaw widok logowania
    login_manager.login_view = 'main.index'  # Zmień na 'auth.login', gdy będzie blueprint auth

    # Funkcja user_loader
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Rejestracja modeli (dla migracji)
    from . import models

    # Import i rejestracja tras/blueprintów
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
