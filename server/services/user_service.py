from server import db
from server.models import User, Task
from datetime import datetime, timedelta
from server.task_modes import TaskMode

def register_user(username, client_id, ip_addr, op_system):
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
    
    if not User.query.filter_by(client_id=client_id).first(): 
        new_user = User(username=username, client_id=client_id)
        new_user.ip_address = ip_addr
        new_user.op_system = op_system
        
        db.session.add(new_user)
        # db.session.commit()
        
    db.session.commit()
    
    return {"status": "SUCCESS", "client_id": client_id}