from flask import Blueprint, request, jsonify, make_response, current_app, render_template
from flask_login import login_required, login_user, logout_user, current_user
from . import roles_required
from ..models import User, Role, RolesUsers, ServiceTask, ServiceTaskUsers, Comment, Ticket, TicketStateEnum, db

from .admin_forms import CreateCityManager

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin_dashboard", methods=["GET"])
@login_required
@roles_required(["admin"])
def admin_dashboard():
    return render_template("admin/admin_dashboard.html", current_user=current_user)


@admin_bp.route("/create_city_manager", methods=["GET", "POST"])
@login_required
@roles_required(["admin"])
def create_city_manager():
    create_city_manager_form = CreateCityManager()
    if request.method == "POST":
        if create_city_manager_form.validate():
            response_object = {
                "status": "success", "message": "Form verification successful"
            }
            return jsonify(response_object), 200
        else:
            return jsonify(create_city_manager_form.errors), 400
    return render_template("admin/create_city_manager.html", current_user=current_user, form=create_city_manager_form)