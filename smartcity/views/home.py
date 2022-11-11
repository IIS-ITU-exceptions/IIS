from flask import Blueprint, render_template
from flask_login import current_user, login_required
from . import roles_required
from ..models import Role, User

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def index():
    roles = Role.query.all()
    if current_user.is_anonymous:
        users = None
    else:
        users = User.query.filter_by(email=current_user.email).first()
    return render_template("public/index.html", roles=roles, users=users, current_user=current_user)
