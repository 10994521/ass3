from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ENUM


import event

# unchanged. Don't think it's necessary
topics = ('Business', 'Mental Health', 'Technology')
topic_enum = ENUM(*topics, name="topics")

statuss = ('Upcoming', 'Cancelled', 'Inactive', 'Booked')
status_enum = ENUM(*statuss,  name="statuss")


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # unique doesn't work for some reason?
    emailid = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(225), nullable=False)

    events = db.relationship('Event', backref='user')
    comments = db.relationship('Comment', backref='user')
    orders = db.relationship('Orders', backref='user')

# edited to be relevant to events. Status column incomplete


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Enum("Business", "Mental Health",
                      "Technology", name="topic"))
    name = db.Column(db.String(80))
    speaker = db.Column(db.String(80))
    description = db.Column(db.String(200))
    dateTime = db.Column(db.DateTime, default=datetime.now())
    address = db.Column(db.String(200))
    image = db.Column(db.String(400))
    tickets = db.Column(db.Integer)
    status = db.Column(db.Enum('Upcoming', 'Cancelled',
                       'Inactive', 'Booked', name="status"), default='Upcoming')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('Orders', backref='event')

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


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    Quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now())
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Order: {}>".format(self.text)
