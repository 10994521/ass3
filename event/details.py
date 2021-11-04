# copied from the class example. Being modified for events.

# import blueprint from flask
from os import waitpid
from flask import Blueprint, render_template, request, redirect, url_for
from flask.helpers import flash
from sqlalchemy.orm import defaultload
from .models import Event, Comment, User, Orders
from flask_login import login_required, current_user
from .forms import CommentForm, OrderForm
from . import db
import time
from sqlalchemy import update

detailsbp = Blueprint('details', __name__, url_prefix='/details')


# this blueprint has been fully updated


@detailsbp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    event = Event.query.filter_by(id=id).first()
    # create the comment form
    cform = CommentForm()
    oform = OrderForm()
    return render_template('/events/details.html', event=event, cform=cform, oform=oform)


@detailsbp.route('/<event>/comment', methods=['GET', 'POST'])
# creates a commont on a certain destination
def comment(event):
    # using the comment form
    form = CommentForm()
    # get the destination object associated to the page and the comment
    event_obj = Event.query.filter_by(id=event).first()
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(user=current_user, text=form.text.data,
                          event=event_obj)
        # here the back-referencing works - comment.destination is set
        # and the link is created
        db.session.add(comment)
        db.session.commit()

        # flashing a message which needs to be handled by the html
        # flash('Your comment has been added', 'success')
        print('Your comment has been added', 'success')
    # using redirect sends a GET request to destination.show
    return redirect(url_for('details.show', id=event))


@detailsbp.route('/<event>/order', methods=['GET', 'POST'])
def order(event):
    form = OrderForm()
    event_obj = Event.query.filter_by(id=event).first()

    if form.validate_on_submit():
        if (form.tickets.data > event_obj.tickets):
            flash('Not enough tickets left')
            return redirect(url_for('details.show', id=event))
        order = Orders(user=current_user,
                       Quantity=form.tickets.data, event=event_obj)
        db.session.add(order)
        db.session.commit()

        formEvent = Event(
            name=event_obj.name,
            speaker=event_obj.speaker,
            description=event_obj.description,
            dateTime=event_obj.dateTime,
            address=event_obj.address,
            image=event_obj.image,
            topic=event_obj.topic,
            tickets=event_obj.tickets - form.tickets.data,
            status=event_obj.status,
            user_id=event_obj.user.id)



        event_obj.name = formEvent.name
        event_obj.speaker = formEvent.speaker
        event_obj.description = formEvent.description
        event_obj.dateTime = formEvent.dateTime
        event_obj.address = formEvent.address
        event_obj.image = formEvent.image
        event_obj.topic = formEvent.topic
        event_obj.tickets = formEvent.tickets
        event_obj.status = formEvent.status

        if formEvent.tickets == 0:
            event_obj.status = "Booked"
        # sqllite can't update two things at once
        db.session.commit()

        flash('Your order has been added, success')
    return redirect(url_for('details.show', id=event))

# didnt change this as i dont think we need to
# def check_upload_file(form):
#   fp = form.image.data
#   filename = fp.filename

#   BASE_PATH = os.path.dirname(__file__)
#   #upload file location – directory of this file/static/image
#   upload_path=os.path.join(BASE_PATH,'static/images',secure_filename(filename))
#   #store relative path in DB as image location in HTML is relative
#   db_upload_path='/static/images/' + secure_filename(filename)
#   #save the file and return the db upload path
#   fp.save(upload_path)
#   return db_upload_path
