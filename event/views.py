from flask import Blueprint, render_template
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
