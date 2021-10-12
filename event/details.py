#copied from the class example. Being modified for events.

#import blueprint from flask
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename

detailsbp = Blueprint('details', __name__, url_prefix ='/details')

#this blueprint has been fully updated
@detailsbp.route('/<id>')
def show(id):
    #event = Event.query.filter_by(id=id).first()
    # create the comment form
    cform = CommentForm()
    return render_template('events/details.html', form = cform)

#needs to be modified so that it will work for both creation and updating(?)
# @eventbp.route('/create', methods = ['GET', 'POST'])
# def create():
#   print('Method type: ', request.method)
#   form = EventForm() #form needs to be made. 
#   if form.validate_on_submit():
#     db_file_path=check_upload_file(form)
#     event = Event(name=form.name.data,
#     speaker=form.speaker.data,
#     description= form.description.data,
#     dateTime=form.date_time.data,
#     address=form.address.data,
#     image=db_file_path,
#     status=form.status.data)
#     # add the object to the db session
#     db.session.add(event)
#     # commit to the database
#     db.session.commit()
#     print('Successfully created new event', 'success')
#     return redirect(url_for('event.create'))
#   return render_template('events/event-manage.html', form=form)

#this blueprint has been updated. Comment form may need to be altered for relevance in forms.py
@detailsbp.route('/<event>/comment', methods = ['GET', 'POST'])
def comment(event):
  #here the form is created  form = CommentForm()
  form = CommentForm()#needs to be modified for ass maybe
  event_obj = Event.query.filter_by(id=event).first()  
  if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        event=event_obj) 
      #here the back-referencing works - comment.event is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit()
      print('Your comment has been added', 'success')
  # notice the signature of url_for
  return redirect(url_for('event.show', id=event))

#didnt change this as i dont think we need to
def check_upload_file(form):
  fp = form.image.data
  filename = fp.filename

  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='/static/image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

