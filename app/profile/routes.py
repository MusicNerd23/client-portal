from flask import render_template
from flask_login import login_required, current_user
from . import profile


@profile.route('/profile')
@login_required
def view_profile():
    return render_template('auth/profile.html')

