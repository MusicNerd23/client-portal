from flask import Blueprint, render_template
from flask_login import login_required
from ..security import role_required

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
@role_required('jusb_admin')
def index():
    return render_template('admin/index.html')
