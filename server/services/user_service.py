from server import db
from server.models import User, Task
from datetime import datetime, timedelta
from server.task_modes import TaskMode

def register_user(username, client_id):
    status = "Successfully registered." # Debugging purposes
    
    # Dummy Task
    dummy_command = "Write-Host -ForegroundColor Red '####################'"
    dummy_task = Task(
        client_id=client_id,
        command=dummy_command,
        command_mode=TaskMode.IN_MEMORY_PS.value,
        repeat_interval=60,
        run_once=False,
        next_execution=datetime.utcnow() + timedelta(seconds=30)
    )
    db.session.add(dummy_task)
    
    if User.query.filter_by(client_id=client_id).first():
        status = "Already registered, reconnecting..."
    else:    
        new_user = User(username=username, client_id=client_id)
        db.session.add(new_user)
        # db.session.commit()
        
    db.session.commit()
    
    return {"status": status} # Debugging purposes