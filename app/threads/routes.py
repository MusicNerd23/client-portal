from flask import Blueprint, render_template
from flask_login import login_required

threads = Blueprint('threads', __name__)

@threads.route('/')
@login_required
def index():
    return render_template('threads/index.html')
