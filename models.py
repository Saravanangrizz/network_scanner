from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
     __tablename__ = 'users'
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(80), unique=True, nullable=False)
     password = db.Column(db.String(512), nullable=False)

class Scan(db.Model):
     __tablename__ = 'scans'
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
     ip_address = db.Column(db.String(255), nullable=False)
     open_ports = db.Column(db.Text, nullable=False)
     timestamp = db.Column(db.DateTime, server_default=db.func.now())

