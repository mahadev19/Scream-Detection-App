from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(256))
    phone = db.Column(db.String(20))

    detections = db.relationship('Detection', backref='user', lazy=True)

class Detection(db.Model):
    __tablename__ = 'detection'
    id = db.Column('detection_id', db.Integer, primary_key=True)
    user_id = db.Column('detection_user_id', db.Integer)
    timestamp = db.Column('detection_timestamp', db.DateTime)
    confidence = db.Column('confidence', db.Float)  # Note no 'detection_' prefix
    location = db.Column('detection_location', db.String(255))
    alert_sent = db.Column('alert_sent', db.Boolean)  # Matches DB column
    audio_path = db.Column('audio_path', db.String(255))  # Matches DB column