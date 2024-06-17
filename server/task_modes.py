from enum import Enum

class TaskMode(Enum):
    FILE_UPLOAD = "FUP"         # Uploads file (as is) to target machine
    FILE_DOWNLOAD = "FDL"       # Downloads a file from the target machine
    COMMAND = "CMD"             # Runs a command on target machine's terminal.
    IN_MEMORY_PS = "IMP"        # Invokes a powershell script in memory (without writing to the disk)
    
    