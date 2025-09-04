from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from ..security import role_required, roles_required
from ..models import Organization, Activity, User
from ..tenancy import current_org_id
from ..extensions import db
from .forms import OrgUserCreateForm, OrgUserDeleteForm

org = Blueprint('org', __name__)

@org.route('/dashboard')
@login_required
def dashboard():
    org_id = current_org_id()
    if not org_id:
        from flask import abort
        abort(403)
    organization = db.session.get(Organization, org_id)
    if not organization:
        from flask import flash, redirect
        flash('Your account is not linked to an organization. Please contact support.')
        return redirect(url_for('index'))
    recent = Activity.query.filter_by(org_id=org_id).order_by(Activity.created_at.desc()).limit(20).all()
    return render_template('org/dashboard.html', organization=organization, recent=recent)

@org.route('/<int:org_id>/dashboard')
@login_required
@role_required('jusb_admin')
def dashboard_scoped(org_id):
    # Admin-only view of a specific organization's dashboard
    organization = db.session.get(Organization, org_id)
    recent = Activity.query.filter_by(org_id=org_id).order_by(Activity.created_at.desc()).limit(20).all()
    return render_template('org/dashboard.html', organization=organization, recent=recent)


@org.route('/users', methods=['GET', 'POST'])
@login_required
@roles_required('client_admin', 'jusb_admin')
def users():
    org_id = current_org_id()
    organization = db.session.get(Organization, org_id)
    form = OrgUserCreateForm()
    delete_form = OrgUserDeleteForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            flash('Email already exists')
            return redirect(url_for('org.users'))
        user = User(email=form.email.data, role=form.role.data, org_id=org_id)
        if form.password.data:
            user.set_password(form.password.data)
        else:
            user.set_password('password')
        db.session.add(user)
        db.session.commit()
        flash('User added to organization')
        return redirect(url_for('org.users'))

    users = User.query.filter_by(org_id=org_id).order_by(User.created_at.desc()).all()
    return render_template('org/users.html', organization=organization, users=users, form=form, delete_form=delete_form)


@org.route('/users/<int:user_id>/remove', methods=['POST'])
@login_required
@roles_required('client_admin', 'jusb_admin')
def users_remove(user_id):
    org_id = current_org_id()
    user = db.session.get(User, user_id)
    if user.org_id != org_id:
        flash('Cannot modify users from another organization')
        return redirect(url_for('org.users'))
    db.session.delete(user)
    db.session.commit()
    flash('User removed')
    return redirect(url_for('org.users'))