# copied from the class example. Being modified for events.

# import blueprint from flask
from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Event, Comment, User
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename

managebp = Blueprint('manage', __name__, url_prefix='/manage')

# this blueprint has been fully updated


@managebp.route('/<id>')
def show(id):
    user = User.query.filter_by(id=id).first()
    return render_template('/events/events.html', user=user)


@managebp.route('/create/<id>', methods=['GET', 'POST'])
def create(id):  # attempted to add creating user to databse
    print('Method type: ', request.method)
    form = EventForm()  # form needs to be made.
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        # creating_user = User.query.filter_by(id=id)#attempted to add creating user to databse
        event = Event(
            name=form.name.data,
            speaker=form.speaker.data,
            description=form.description.data,
            dateTime=form.date_time.data,
            address=form.address.data,
            image=db_file_path,
            topic=form.topic.data,
            tickets=form.tickets.data,
            price=form.price.data,
            status=form.status.data,
            user_id=id)  # attempted to add creating user to databse
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        print('Successfully created new event', 'success')
        return redirect(url_for('details.show', id=event.id))
    return render_template('/events/event-manage.html', form=form)


@managebp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):  # attempted to add creating user to databse
    print('Method type: ', request.method)
    event = Event.query.filter_by(id=id).first()
    # pass through event to prefil form with existing data
    form = EventForm(obj=event)

    # form.name.data = event.name
    # form.speaker.data = event.speaker
    # form.description.data = event.description
    # form.date_time.data = event.dateTime
    # form.address.data = event.address
    # db_file_path = event.image
    # form.status.data = event.status

    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        # creating_user = User.query.filter_by(id=id)#attempted to add creating user to databse
        formEvent = Event(
            name=form.name.data,
            speaker=form.speaker.data,
            description=form.description.data,
            dateTime=form.date_time.data,
            address=form.address.data,
            image=db_file_path,
            topic=form.topic.data,
            tickets=form.tickets.data,
            price=form.price.data,
            status=form.status.data,
            user_id=id)  # attempted to add creating user to databse

        # change each attribute to new values
        event.name = formEvent.name
        event.speaker = formEvent.speaker
        event.description = formEvent.description
        event.dateTime = formEvent.dateTime
        event.address = formEvent.address
        event.image = formEvent.image
        event.topic = formEvent.topic
        event.tickets = formEvent.tickets
        event.price = formEvent.price
        event.status = formEvent.status

        # commit to the database
        db.session.commit()
        print('Successfully edited event', 'success')
        return redirect(url_for('details.show', id=event.id))
    return render_template('/events/event-manage.html', form=form)
# this blueprint has been updated. Comment form may need to be altered for relevance in forms.py


# NEEDS TO BE FINISHED, COULDN'T WORK IT OUT
@managebp.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):  # attempted to add creating user to databse
    print('Method type: ', request.method)
    event = Event.query.filter_by(id=id).first()
    # commit to the database
    Comment.query.filter(Comment.event_id == id).delete()
    db.session.delete(event)
    db.session.commit()

    return render_template('/index.html')


def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename

    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, 'static/images', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/images/' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path
