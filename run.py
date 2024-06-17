from server import create_server

if __name__ == "__main__":
    server = create_server()
    server.run(host="localhost", port=9393)