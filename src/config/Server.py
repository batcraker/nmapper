from flask import Flask
from uuid import uuid4

class Server:
    def __init__(self, port=3000) -> None:
        self.app = Flask(__name__, template_folder='../../templates', static_folder='../../static')
        self.app.secret_key=uuid4().__str__()
        self.port = port
    
    def run(self, debug=False):
        self.app.run(port=self.port, debug=debug)