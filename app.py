from tools.Nmapper import Nmapper
import json
from tools.Server import Server
from flask import render_template, jsonify, request
from routes import api
import os
import requests


app = Server()
@app.app.route("/")
def home():
    # Listing dir content
    files = []

    for file in os.listdir('./uploads'):
        if os.path.isfile(os.path.join('./uploads',file)):
            files.append(file)        

    return render_template("home.html", files=files)

@app.app.route("/file/<filename>")
def nmapper(filename):
    uri = f"http://localhost:3000/api/nmapper/{filename}?"
    # Get args from response
    getWithOpenPorts = request.args.get('openPorts')
    getWithDomainName = request.args.get('domainNames')
    if getWithOpenPorts:
        uri += f"openPorts={getWithOpenPorts}&"
    if getWithDomainName:
        uri += f"domainNames={getWithDomainName}&"

    response = requests.get(f"{uri}")
    response_json = response.json()

    return render_template("viewer.html", file=filename, data=response_json)

    
#register the blueprint
app.app.register_blueprint(api)


if __name__ == '__main__':
    app.run(debug=True)
