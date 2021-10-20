# copied from the class example. Being modified for events.

# import blueprint from flask
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.orm import defaultload
from .models import Event, Comment, User
from flask_login import login_required, current_user
from .forms import CommentForm
from . import db

detailsbp = Blueprint('details', __name__, url_prefix='/details')


# this blueprint has been fully updated


@detailsbp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    event = Event.query.filter_by(id=id).first()
    # create the comment form
    cform = CommentForm()
    return render_template('/events/details.html', event=event, form=cform)

# needs to be modified so that it will work for both creation and updating(?)
# @eventbp.route('/create', methods = ['GET', 'POST'])
# def create():
#   print('Method type: ', request.method)
#   form = EventForm()
#   if form.validate_on_submit():
#      db_file_path=check_upload_file(form)
#      event = Event(name=form.name.data,
#      speaker=form.speaker.data,
#      description= form.description.data,
#      dateTime=form.date_time.data,
#      address=form.address.data,
#      image=db_file_path,
#      status=form.status.data)
#      # add the object to the db session
#      db.session.add(event)
#      # commit to the database
#      db.session.commit()
#      print('Successfully created new event', 'success')
#      return redirect(url_for('details.show', id = event.id))
#   return render_template('', form=form)

# this blueprint has been updated. Comment form may need to be altered for relevance in forms.py


@detailsbp.route('/<event>/comment', methods=['GET', 'POST'])
# creates a commont on a certain destination
def comment(event):
    # using the comment form
    form = CommentForm()
    print("aaaaaaaaa")
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
        #flash('Your comment has been added', 'success')
        print('Your comment has been added', 'success')
    # using redirect sends a GET request to destination.show
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
