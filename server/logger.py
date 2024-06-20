from . import db
from server.models import Log
from enum import Enum
from datetime import datetime

class LogLevel(Enum):
    INFO = "info"       # General operational messages
    WARNING = "warning" # Could lead to errors if not monitored
    ERROR = "error"     # Error conditions that need addressing
    ALERT = "alert"     # General messages that are more relevant than 'info'
    REPORT = "report"   # Result recieved from the /report endpoint.

class Logger():
    @staticmethod
    def log(client_id, log_level, message):
        log_entry = Log(client_id=client_id, log_level=log_level, message=message, timestamp=datetime.utcnow())
        db.session.add(log_entry)
        db.session.commit()