from functools import wraps
from flask import abort
from flask_login import current_user

def org_scoped_query(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        org_id = kwargs.get('org_id')
        if not org_id or org_id != current_user.org_id:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
