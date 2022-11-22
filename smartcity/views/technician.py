from sqlalchemy import desc
from flask import Blueprint, request, jsonify, make_response, current_app, render_template
from flask_login import login_required, login_user, logout_user, current_user

from smartcity.views import roles_required
from smartcity.models import User, Role, RolesUsers, ServiceTask, ServiceTaskUsers, Comment, Ticket, TicketStateEnum, db


technician_bp = Blueprint("technician", __name__)


@technician_bp.route("/assigned_tasks", methods=["GET"])
@login_required
@roles_required(["technician"])
def assigned_tasks():
    service_tasks = ServiceTask.query.join(ServiceTaskUsers).filter(ServiceTaskUsers.user_id == current_user.id).all()
    return render_template("technician/assigned_tasks.html", current_user=current_user, service_tasks=service_tasks)

@technician_bp.route("/task_view", methods=["GET"])
@login_required
@roles_required(["technician"])
def task_view():
    if request.method == "GET":
        ticket_comments = Comment.query.filter_by(ticket_id=request.args.get("ticketId")).all()
        try:
            selected_ticket_id = int(request.args.get("ticketId"))
        except Exception as e:
            return render_template("204.html")
    tickets = Ticket.query.filter(Ticket.assignee_id == current_user.id, Ticket.state != 'New').all()
    return render_template("technician/task_view.html", current_user=current_user, tickets=tickets)
