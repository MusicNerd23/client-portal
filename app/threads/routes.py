import os
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from ..models import Thread, Message, File
from ..extensions import db, limiter
from .forms import ThreadForm, MessageForm
from ..files.routes import allowed_file
from ..storage import get_storage
from ..models import record_activity
from ..tenancy import current_org_id
from ..models import User, Message as MessageModel
from ..notifications import send_email

threads = Blueprint('threads', __name__)

@threads.route('/', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
@login_required
def index():
    form = ThreadForm()
    if form.validate_on_submit():
        org_id = current_org_id()
        thread = Thread(title=form.title.data, org_id=org_id, created_by=current_user.id)
        db.session.add(thread)
        db.session.flush()
        record_activity('thread.create', 'Thread', thread.id)
        db.session.commit()
        flash('Your thread has been created!')
        return redirect(url_for('threads.index'))
    org_id = current_org_id()
    all_threads = Thread.query.filter_by(org_id=org_id).all()
    return render_template('threads/index.html', threads=all_threads, form=form)

@threads.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
@limiter.limit("60 per minute")
@login_required
def view_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    # Enforce org scoping: clients can only access their org's threads.
    allowed_org_id = current_org_id()
    if thread.org_id != allowed_org_id and current_user.role != 'jusb_admin':
        abort(403)
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(body=form.body.data, thread_id=thread.id, author_id=current_user.id)
        # Handle optional attachment
        file = request.files.get('attachment')
        if file and file.filename:
            if allowed_file(file.filename):
                storage = get_storage()
                org_slug = current_user.organization.slug
                file_path, filename = storage.save(org_slug, file)
                new_file = File(
                    org_id=current_user.org_id,
                    uploader_id=current_user.id,
                    filename=filename,
                    path=file_path,
                    mime=file.mimetype,
                    size=os.path.getsize(file_path)
                )
                db.session.add(new_file)
                db.session.flush()
                message.attachments = {"file_ids": [new_file.id]}
            else:
                flash('Attachment type not allowed')
                return redirect(url_for('threads.view_thread', thread_id=thread.id))
        db.session.add(message)
        db.session.flush()
        record_activity('message.create', 'Message', message.id)
        db.session.commit()
        # Notify other participants and org admins
        try:
            participant_ids = [row.author_id for row in MessageModel.query.with_entities(MessageModel.author_id).filter_by(thread_id=thread.id).distinct().all()]
            recipient_users = User.query.filter(User.id.in_(participant_ids), User.id != current_user.id).all()
            admin_users = User.query.filter_by(org_id=thread.org_id, role='client_admin').all()
            recipients = {u.email for u in recipient_users + admin_users}
            if recipients:
                send_email(
                    subject=f"New message in: {thread.title}",
                    body=f"{current_user.email} wrote:\n\n{message.body}",
                    recipients=list(recipients),
                )
        except Exception:
            pass
        flash('Your message has been sent!')
        return redirect(url_for('threads.view_thread', thread_id=thread.id))
    
    messages = Message.query.filter_by(thread_id=thread.id).order_by(Message.created_at.asc()).all()
    return render_template('threads/view_thread.html', thread=thread, messages=messages, form=form)
