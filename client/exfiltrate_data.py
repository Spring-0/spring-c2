import os
import getpass
import platform
import socket
import psutil
import json

class DataExfiltrator:
    def __init__(self):
        self.data_modules = []
        
    def gather_system_info(self):
        try:
            username = getpass.getuser()
            hostname = socket.gethostname()
            ip_addr = socket.gethostbyname(hostname)
            sys_data = platform.uname()
            
            system_info = {
                "username": username,
                "hostname": hostname,
                "ip_addr": ip_addr,
                "system": sys_data.system,
                "node_name": sys_data.node,
                "release": sys_data.release,
                "version": sys_data.version,
                "machine": sys_data.machine,
                "processor": sys_data.processor
            }
            
            self.data_modules.append(system_info)
            
        except Exception as e:
            print(f"Error gathering system info: {str(e)}")
            
    def gather_machine_info(self):
        try:
            cpu_info = platform.processor()
            cpu_count = psutil.cpu_count(logical=False)
            logical_cpu_count = psutil.cpu_count(logical=True)
            
            disk_info = psutil.disk_usage("/")
            
            machine_info = {
                "cpu_count": os.cpu_count(),
                "total_memory": psutil.virtual_memory().total,
                "cpu_processor": cpu_info,
                "cpu_physical_cores": cpu_count,
                "cpu_logical_cores": logical_cpu_count,
                "disk_total_space": disk_info.total,
                "disk_used_space": disk_info.used,
                "disk_free_space": disk_info.free,
                "disk_space_utilization": disk_info.percent
            }
            
            self.data_modules.append(machine_info)
        except Exception as e:
            print(f"Error gathering machine info: {str(e)}")
            
    def get_data(self):
        return json.dumps(self.data_modules)