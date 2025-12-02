from models import Detection
from extensions import db
from datetime import datetime

def log_detection(user_id, confidence, location, alert_sent):
    detection = Detection(
        user_id=user_id,
        timestamp=datetime.utcnow(),
        confidence=confidence,
        location=location,
        alert_sent=alert_sent
    )
    db.session.add(detection)
    db.session.commit()
