from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Task
from ..extensions import db
from .forms import TaskForm

tasks = Blueprint('tasks', __name__)

@tasks.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data, org_id=current_user.org_id)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!')
        return redirect(url_for('tasks.index'))
    
    all_tasks = Task.query.all()
    return render_template('tasks/index.html', tasks=all_tasks, form=form)
