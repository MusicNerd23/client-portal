from flask import Blueprint, render_template
from flask_login import login_required

files = Blueprint('files', __name__)

@files.route('/')
@login_required
def index():
    return render_template('files/index.html')
