from . import db
import uuid
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(36), unique=True, nullable=False,           # Machine identifier
                          default="[SERVER-GENERATED] " + str(uuid.uuid4()))
    username = db.Column(db.String(20), unique=False, nullable=True)            # Machine account username
    last_beacon_signal = db.Column(db.DateTime, default=datetime.utcnow)        # Time when last beacon signal was recieved
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(36), nullable=False)
    command = db.Column(db.String(255), nullable=False)                  # Command to be executed on client_id machine
    repeat_interval = db.Column(db.Integer)                              # Interval in seconds to repeat command execution (if repeating)
    run_once = db.Column(db.Boolean, default=False)                      # Flag to determine if task should run once
    next_execution = db.Column(db.DateTime, default=datetime.utcnow())   # Next scheduled execution