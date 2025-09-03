from flask import Blueprint, render_template
from flask_login import login_required

tasks = Blueprint('tasks', __name__)

@tasks.route('/')
@login_required
def index():
    return render_template('tasks/index.html')
