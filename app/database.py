from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    conversions = db.relationship(
        "Conversion", back_populates="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Conversion(db.Model):
    __tablename__ = "conversions"

    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255), nullable=False)
    document_title = db.Column(db.String(255))
    status = db.Column(db.String(50), default="success")
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    output_filename = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="conversions")

    def __repr__(self):
        return f"<Conversion {self.original_filename} [{self.status}]>"


class CourseMetadata(db.Model):
    __tablename__ = "course_metadata"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    conversion_id = db.Column(db.Integer, db.ForeignKey(
        "conversions.id"), nullable=False)

    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(255), nullable=True)
    organization = db.Column(db.String(255), nullable=True)
    language = db.Column(db.String(10), default="ru")
    version = db.Column(db.String(20), default="1.0")
    keywords = db.Column(db.String(500), nullable=True)

    user = db.relationship("User", backref="metadata_entries")
    conversion = db.relationship(
        "Conversion", backref="metadata", uselist=False)
