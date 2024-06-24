from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from server.config import Config
from flask_cors import CORS

db = SQLAlchemy()

def create_server():
    server = Flask(__name__)
    
    apply_server_configuration(server)
    db.init_app(server)
    
    with server.app_context():
        from . import routes
        server.register_blueprint(routes.bp)
        CORS(server)
        
        db.create_all()
        
    return server

def apply_server_configuration(server):
    server.config["SQLALCHEMY_DATABASE_URI"] = Config.get("database", "uri")
    server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    