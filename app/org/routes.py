from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Organization

org = Blueprint('org', __name__)

@org.route('/dashboard')
@login_required
def dashboard():
    organization = Organization.query.get(current_user.org_id)
    return render_template('org/dashboard.html', organization=organization)
