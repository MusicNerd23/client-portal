from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from ..models import Ticket, TicketComment, User, record_activity
from ..extensions import db, limiter
from ..tenancy import current_org_id
from .forms import TicketForm, TicketStatusForm, TicketCommentForm, TicketAssignForm
from ..notifications import send_email

tickets = Blueprint('tickets', __name__)


@tickets.route('/', methods=['GET', 'POST'])
@login_required
@limiter.limit("20 per minute")
def index():
    form = TicketForm()
    status_form = TicketStatusForm()
    if form.validate_on_submit():
        t = Ticket(
            org_id=current_org_id(),
            created_by_id=current_user.id,
            subject=form.subject.data,
            description=form.description.data,
            priority=form.priority.data,
            status='new',
        )
        db.session.add(t)
        db.session.flush()
        record_activity('ticket.create', 'Ticket', t.id)
        db.session.commit()
        # Notify org admins
        try:
            admins = User.query.filter_by(org_id=t.org_id, role='client_admin').all()
            recipients = [u.email for u in admins]
            if recipients:
                send_email(
                    subject=f"New ticket #{t.id}: {t.subject}",
                    body=f"Created by {current_user.email}\nPriority: {t.priority}\n\n{t.description or ''}",
                    recipients=recipients,
                )
        except Exception:
            pass
        flash('Ticket created')
        return redirect(url_for('tickets.index'))

    org_id = current_org_id()
    q = Ticket.query.filter_by(org_id=org_id)
    status = request.args.get('status')
    priority = request.args.get('priority')
    if status:
        q = q.filter(Ticket.status == status)
    if priority:
        q = q.filter(Ticket.priority == priority)
    all_tickets = q.order_by(Ticket.created_at.desc()).all()
    return render_template('tickets/index.html', tickets=all_tickets, form=form, status_form=status_form)


@tickets.route('/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
@limiter.limit("60 per minute")
def view(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.org_id != current_org_id() and current_user.role != 'jusb_admin':
        abort(403)
    comment_form = TicketCommentForm()
    status_form = TicketStatusForm()
    assign_form = TicketAssignForm()
    # Populate assignee choices with org users
    org_users = User.query.filter_by(org_id=ticket.org_id).order_by(User.email.asc()).all()
    assign_form.assignee.choices = [(0, 'Unassigned')] + [(u.id, u.email) for u in org_users]
    if comment_form.validate_on_submit():
        c = TicketComment(ticket_id=ticket.id, author_id=current_user.id, body=comment_form.body.data)
        db.session.add(c)
        db.session.flush()
        record_activity('ticket.comment', 'Ticket', ticket.id)
        db.session.commit()
        # Notify creator and assignee (excluding commenter)
        try:
            recipients = set()
            if ticket.created_by and ticket.created_by.email and ticket.created_by_id != current_user.id:
                recipients.add(ticket.created_by.email)
            if ticket.assigned_to and ticket.assigned_to.email and ticket.assigned_to_id != current_user.id:
                recipients.add(ticket.assigned_to.email)
            if recipients:
                send_email(
                    subject=f"Update on ticket #{ticket.id}: {ticket.subject}",
                    body=f"{current_user.email} commented:\n\n{c.body}",
                    recipients=list(recipients),
                )
        except Exception:
            pass
        flash('Comment added')
        return redirect(url_for('tickets.view', ticket_id=ticket.id))

    comments = TicketComment.query.filter_by(ticket_id=ticket.id).order_by(TicketComment.created_at.asc()).all()
    return render_template('tickets/view.html', ticket=ticket, comments=comments, comment_form=comment_form, status_form=status_form, assign_form=assign_form)


@tickets.route('/<int:ticket_id>/status', methods=['POST'])
@login_required
def update_status(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.org_id != current_org_id() and current_user.role != 'jusb_admin':
        abort(403)
    form = TicketStatusForm()
    if form.validate_on_submit():
        ticket.status = form.status.data
        db.session.flush()
        record_activity('ticket.update_status', 'Ticket', ticket.id)
        db.session.commit()
        # Notify creator and assignee
        try:
            recipients = set()
            if ticket.created_by and ticket.created_by.email and ticket.created_by_id != current_user.id:
                recipients.add(ticket.created_by.email)
            if ticket.assigned_to and ticket.assigned_to.email and ticket.assigned_to_id != current_user.id:
                recipients.add(ticket.assigned_to.email)
            if recipients:
                send_email(
                    subject=f"Status updated for ticket #{ticket.id}: {ticket.subject}",
                    body=f"New status: {ticket.status}\nChanged by: {current_user.email}",
                    recipients=list(recipients),
                )
        except Exception:
            pass
        flash('Status updated')
    else:
        flash('Invalid status update')
    return redirect(url_for('tickets.view', ticket_id=ticket.id))


@tickets.route('/<int:ticket_id>/assign', methods=['POST'])
@login_required
def assign(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.org_id != current_org_id() and current_user.role != 'jusb_admin':
        abort(403)
    form = TicketAssignForm()
    if form.validate_on_submit():
        ticket.assigned_to_id = form.assignee.data or None
        db.session.flush()
        record_activity('ticket.assign', 'Ticket', ticket.id)
        db.session.commit()
        # Notify creator and new assignee
        try:
            recipients = set()
            if ticket.created_by and ticket.created_by.email and ticket.created_by_id != current_user.id:
                recipients.add(ticket.created_by.email)
            if ticket.assigned_to and ticket.assigned_to.email and ticket.assigned_to_id != current_user.id:
                recipients.add(ticket.assigned_to.email)
            if recipients:
                send_email(
                    subject=f"Assignment updated for ticket #{ticket.id}: {ticket.subject}",
                    body=f"Assigned to: {ticket.assigned_to.email if ticket.assigned_to else '—'}\nChanged by: {current_user.email}",
                    recipients=list(recipients),
                )
        except Exception:
            pass
        flash('Assignment updated')
    else:
        flash('Invalid assignment')
    return redirect(url_for('tickets.view', ticket_id=ticket.id))
