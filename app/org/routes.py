from flask import Blueprint, render_template
from flask_login import login_required

org = Blueprint('org', __name__)

@org.route('/dashboard')
@login_required
def dashboard():
    return render_template('org/dashboard.html')
