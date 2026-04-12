from flask import Flask
from app.database import db


def create_app():
    app = Flask(__name__, template_folder="../web")

    app.secret_key = "замени-на-случайную-строку"

    # Настройка БД — файл scorm.db появится в корне проекта
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scorm.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Инициализируем SQLAlchemy с приложением
    db.init_app(app)

    # Создаём таблицы если их ещё нет
    with app.app_context():
        db.create_all()

    from app.routes import bp
    app.register_blueprint(bp)

    return app