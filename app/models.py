from datetime import datetime
from flask_login import UserMixin
from .utilities.db import db


class User(db.Model, UserMixin):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    categories = db.relationship(
        "Category", backref="user", cascade="all, delete-orphan")
    notes = db.relationship("Note", backref="user",
                            cascade="all, delete-orphan")


class Category(db.Model, UserMixin):

    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notes = db.relationship("Note", backref="category",
                            cascade="all, delete-orphan")
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Note(db.Model, UserMixin):

    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
