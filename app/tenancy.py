from functools import wraps
from flask import abort, session
from flask_login import current_user


def current_org_id() -> int | None:
    """Return the effective org_id for the current user.

    - For jusb_admin with an active org switch, return session['admin_org_id'].
    - Otherwise, return current_user.org_id.
    """
    if not current_user.is_authenticated:
        return None
    if current_user.role == 'jusb_admin' and 'admin_org_id' in session:
        return session.get('admin_org_id')
    return current_user.org_id


def org_scoped_query(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        org_id = kwargs.get('org_id')
        effective_org = current_org_id()
        if not org_id or org_id != effective_org:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
