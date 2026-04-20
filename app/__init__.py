from flask import Flask
from flask_login import LoginManager
from app.database import db, User


def create_app():
    app = Flask(__name__, template_folder="../web")

    app.secret_key = "замени-на-случайную-строку"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scorm.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # ← 16 МБ максимум

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    from app.routes import bp
    from app.auth import auth_bp
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)

    return app