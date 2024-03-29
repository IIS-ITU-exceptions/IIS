"""
init file

@author: Dominik Vágner
@email: xvagne10@stud.fit.vutbr.cz
"""

from functools import wraps

from flask import abort
from flask_login import current_user


def roles_required(roles):
    def decorator_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not set(roles).intersection({r.name for r in current_user.role}):
                return abort(401)
            return f(*args, **kwargs)
        return wrapper
    return decorator_function
