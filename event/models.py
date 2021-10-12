from . import db
from datetime import datetime
from flask_login import UserMixin

import event

# unchanged. Don't think it's necessary


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    emailid = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(225), nullable=False)

    events = db.relationship('Event', backref='user')
    comments = db.relationship('Comment', backref='user')

# edited to be relevant to events. Status column incomplete


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    speaker = db.Column(db.String(80))
    description = db.Column(db.String(200))
    dateTime = db.Column(db.DateTime, default=datetime.now())
    address = db.Column(db.String(200))
    image = db.Column(db.String(400))
    status = db.Column(db.Enum('Upcoming','Cancelled','Inactive','Booked'), default='Upcoming')  

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='event')

    def __repr__(self):
        return "<Name: {}>".format(self.name)

# changed occurences of destination to event


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
