from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
metadata =MetaData(naming_convention=naming_convention)

db = SQLAlchemy(metadata=metadata)

class Episode(db.Model, SerializerMixin):
    __tablename__= "episodes"

    serialize_rules = ('-appearances.episode',)
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.now())
    number = db.Column(db.Integer, nullable=False)

    appearances= db.relationship('Appearance', back_populates='episode', cascade='all, delete')

class Appearance(db.Model, SerializerMixin):
    __tablename__= "appearances"

    serialize_rules = ('-episode.appearances', '-guest.appearances')

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id= db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False) 
    guest_id = db.Column(db.Integer,db.ForeignKey("guests.id"),  nullable=False)

    episode= db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')
    @validates('rating')
    def validate_rating(self, key, value):
        allowed_range = range(1, 6)  # 1 to 5 inclusive
        if value not in allowed_range:
            allowed_str = ", ".join(map(str, allowed_range))
            raise ValueError(f"Rating must be between 1 and 5. Allowed values: {allowed_str}")
        return value
class Guest(db.Model, SerializerMixin):
    __tablename__= "guests"

    serialize_rules = ('-appearances.guest',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    occupation = db.Column(db.Text, nullable=False)

    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete')
  


