from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_server():
    server = Flask(__name__)
    server.config.from_object("server.config.Config")
    
    db.init_app(server)
    
    with server.app_context():
        from . import routes
        server.register_blueprint(routes.bp)
        
        db.create_all()
        
    return server