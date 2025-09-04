from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required
from ..security import role_required
from ..models import Organization, User, Ticket
from ..extensions import db

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
@role_required('jusb_admin')
def index():
    organizations = Organization.query.all()
    users = User.query.all()
    return render_template('admin/index.html', organizations=organizations, users=users)

@admin.route('/switch_org/<int:org_id>')
@login_required
@role_required('jusb_admin')
def switch_org(org_id):
    organization = Organization.query.get_or_404(org_id)
    session['admin_org_id'] = org_id
    flash(f'Switched to organization: {organization.name}')
    return redirect(url_for('org.dashboard'))

@admin.route('/clear_switch_org')
@login_required
@role_required('jusb_admin')
def clear_switch_org():
    session.pop('admin_org_id', None)
    flash('Cleared organization switch.')
    return redirect(url_for('org.dashboard'))

@admin.route('/tickets')
@login_required
@role_required('jusb_admin')
def tickets_overview():
    # Basic overview across all orgs
    counts = {
        'new': db.session.query(Ticket).filter_by(status='new').count(),
        'open': db.session.query(Ticket).filter_by(status='open').count(),
        'pending': db.session.query(Ticket).filter_by(status='pending').count(),
        'resolved': db.session.query(Ticket).filter_by(status='resolved').count(),
        'closed': db.session.query(Ticket).filter_by(status='closed').count(),
    }
    recent = Ticket.query.order_by(Ticket.created_at.desc()).limit(25).all()
    return render_template('admin/tickets.html', counts=counts, recent=recent)
