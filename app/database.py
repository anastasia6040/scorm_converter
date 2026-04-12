from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Conversion(db.Model):
    """
    Хранит информацию о каждой конвертации документа.
    """
    __tablename__ = "conversions"

    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255), nullable=False)  # имя загруженного .docx
    document_title = db.Column(db.String(255))                     # заголовок внутри документа
    status = db.Column(db.String(50), default="success")           # "success" или "error"
    error_message = db.Column(db.Text, nullable=True)              # текст ошибки, если была
    created_at = db.Column(db.DateTime, default=datetime.utcnow)   # дата и время конвертации

    def __repr__(self):
        return f"<Conversion {self.original_filename} [{self.status}]>"