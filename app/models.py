from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(21), unique=True, index=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
