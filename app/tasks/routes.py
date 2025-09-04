from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..models import Task
from ..extensions import db
from .forms import TaskForm, TaskStatusForm, TaskDeleteForm
from ..tenancy import current_org_id

tasks = Blueprint('tasks', __name__)

@tasks.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = TaskForm()
    status_form = TaskStatusForm()
    delete_form = TaskDeleteForm()
    if form.validate_on_submit():
        org_id = current_org_id()
        task = Task(title=form.title.data, description=form.description.data, org_id=org_id)
        db.session.add(task)
        db.session.flush()
        from ..models import record_activity
        record_activity('task.create', 'Task', task.id)
        db.session.commit()
        flash('Your task has been created!')
        return redirect(url_for('tasks.index'))

    org_id = current_org_id()
    all_tasks = Task.query.filter_by(org_id=org_id).order_by(Task.created_at.desc()).all()
    return render_template('tasks/index.html', tasks=all_tasks, form=form, status_form=status_form, delete_form=delete_form)


@tasks.route('/<int:task_id>/status', methods=['POST'])
@login_required
def update_status(task_id):
    form = TaskStatusForm()
    task = Task.query.get_or_404(task_id)
    if task.org_id != current_user.org_id and current_user.role != 'jusb_admin':
        abort(403)
    if form.validate_on_submit():
        task.status = form.status.data
        from ..models import record_activity
        db.session.flush()
        record_activity('task.update_status', 'Task', task.id)
        db.session.commit()
        flash('Task status updated')
    else:
        flash('Invalid status update')
    return redirect(url_for('tasks.index'))


@tasks.route('/kanban')
@login_required
def kanban():
    org_id = current_org_id()
    all_tasks = Task.query.filter_by(org_id=org_id).all()
    columns = {
        'open': [t for t in all_tasks if t.status == 'open'],
        'in_progress': [t for t in all_tasks if t.status == 'in_progress'],
        'done': [t for t in all_tasks if t.status == 'done'],
    }
    status_form = TaskStatusForm()
    delete_form = TaskDeleteForm()
    return render_template('tasks/kanban.html', columns=columns, status_form=status_form, delete_form=delete_form)


@tasks.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete(task_id):
    form = TaskDeleteForm()
    task = Task.query.get_or_404(task_id)
    if task.org_id != current_user.org_id and current_user.role != 'jusb_admin':
        abort(403)
    if form.validate_on_submit():
        from ..models import record_activity
        db.session.delete(task)
        db.session.flush()
        record_activity('task.delete', 'Task', task.id)
        db.session.commit()
        flash('Task deleted')
    else:
        flash('Invalid delete request')
    return redirect(url_for('tasks.index'))
