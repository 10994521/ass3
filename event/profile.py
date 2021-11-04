#copied straight from the class example. To be modified if required.


from flask import Blueprint, render_template, request,redirect,url_for,flash
from .forms import LoginForm, RegisterForm
from .models import User

#create a blueprint
profilebp = Blueprint('profile', __name__, url_prefix ='/profile')

@profilebp.route('/<id>')
def show(id):
   user = User.query.filter_by(id=id).first()
   return render_template('/profile.html', user=user)