from flask import Blueprint, request, jsonify, make_response, current_app, render_template
from flask_login import login_required, login_user, logout_user, current_user
from . import roles_required
from ..models import User, Role, RolesUsers, ServiceTask, ServiceTaskUsers, Comment, Ticket, TicketStateEnum, db
from sqlalchemy import desc


technician_bp = Blueprint("technician", __name__)


@technician_bp.route("/assigned_tickets", methods=["GET"])
@login_required
@roles_required(["technician"])
def assigned_tickets():
    tickets = Ticket.query.filter(Ticket.assignee_id == current_user.id, Ticket.state != 'New').all()
    return render_template("technician/assigned_tickets.html", current_user=current_user, tickets=tickets)
