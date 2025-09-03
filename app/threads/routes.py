from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Thread, Message
from ..extensions import db
from .forms import ThreadForm, MessageForm

threads = Blueprint('threads', __name__)

@threads.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ThreadForm()
    if form.validate_on_submit():
        thread = Thread(title=form.title.data, org_id=current_user.org_id, created_by=current_user.id)
        db.session.add(thread)
        db.session.commit()
        flash('Your thread has been created!')
        return redirect(url_for('threads.index'))
    
    all_threads = Thread.query.all()
    return render_template('threads/index.html', threads=all_threads, form=form)

@threads.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def view_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(body=form.body.data, thread_id=thread.id, author_id=current_user.id)
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent!')
        return redirect(url_for('threads.view_thread', thread_id=thread.id))
    
    messages = Message.query.filter_by(thread_id=thread.id).order_by(Message.created_at.asc()).all()
    return render_template('threads/view_thread.html', thread=thread, messages=messages, form=form)
