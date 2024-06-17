from flask import Blueprint, request, jsonify
from .models import User
from . import db
from server.services.user_service import register_user
from server.services.beacon_service import handle_beacon_request

bp = Blueprint("routes", __name__)

@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    client_id = data.get("client_id")
    
    response = register_user(username, client_id)
    return jsonify(response)

@bp.route('/beacon', methods=['POST'])
def beacon():
    data = request.json
    client_id = data.get("client_id")
    
    response = handle_beacon_request(client_id)
    return jsonify(response)

@bp.route('/report', methods=['POST'])
def report():
    data = request.json
    print(f"[+] Report from client: {data}")
    response = {"status": "recieved"}
    return jsonify(response)