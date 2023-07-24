from flask import Flask

class Server:
    def __init__(self, port=3000) -> None:
        self.app = Flask(__name__, template_folder='../templates', static_folder='../static')
        self.port = port
    
    def run(self, debug=False):
        self.app.run(port=self.port, debug=debug)