from server import create_server
from server.config import Config

if __name__ == "__main__":
    server = create_server()
    server.run(
        host=Config.get("server", "host", "localhost"),
        port=Config.get("server", "port", 9393)
    )