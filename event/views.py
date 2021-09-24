from flask import Blueprint, render_template

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    return render_template('index.html')


@mainbp.route('/profile')
def profile():
    return render_template('profile.html')

@mainbp.route('/details')
def details():
    return render_template('details.html')

