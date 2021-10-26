from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)


@mainbp.route('/profile')
def profile():
    return render_template('profile.html')


@mainbp.route('/details')
def details():
    return render_template('details.html')


@mainbp.route('/search')
# on the '/search' url, fetch data from the search form and query destinations with the same description.
# then, returns index html with a new set of destinations
def search():
    if request.args['search'] and request.args['topic']:
        print(request.args['search'])
        print(request.args['topic'])
        evnt = "%" + request.args['search'] + '%'
        evnt2 = "%" + request.args['topic'] + '%'

        events = Event.query.filter(
            Event.name.like(evnt),
            Event.topic.like(evnt2)
        ).all()

    else:
        if request.args['topic']:
            print(request.args['topic'])
            evnt = "%" + request.args['topic'] + '%'
            events = Event.query.filter(
                Event.topic.like(evnt)).all()
        elif request.args['search']:
            print(request.args['search'])
            evnt = "%" + request.args['search'] + '%'
            events = Event.query.filter(
                Event.name.like(evnt)).all()

        else:
            return redirect(url_for('main.index'))

    return render_template('index.html', events=events)
