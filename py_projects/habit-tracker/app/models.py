from app.database import db
from datetime import datetime
from sqlalchemy.orm import validates

class Habit(db.Model):

    __tablename__="habits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @validates('name')
    def validate_name(self, key, value):
        if len(value) > 50:
            raise ValueError("Name must be 50 characters or less.")
        return value
    
    @validates('description')
    def validate_description(self, key, value):
        if value and len(value) > 100:
            raise ValueError("Description must be 100 characters or fewer.")
        return value

    def __repr__(self):
        return f"Habit {self.name}"