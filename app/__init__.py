from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="../web")

    app.secret_key = "замени-на-случайную-строку"

    from app.routes import bp
    app.register_blueprint(bp)

    return app