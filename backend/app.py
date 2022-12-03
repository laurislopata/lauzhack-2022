from flask import Flask, request
import docker
import json
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)


client = docker.from_env()
containers = client.containers.list()


@app.route('/')
@cross_origin()
def hello_world():
    return {"data": "Hello, World!"}

@app.route('/start/<id>')
@cross_origin()
def start_container(id):
    for container in containers:
        if container.id == id:
            container.unpause()
    return "Container started"

@app.route('/stop/<id>')
@cross_origin()
def stop_container(id):
    for container in containers:
        if container.id == id:
            container.pause()
    return "Container paused"

@app.route('/kill/<id>')
@cross_origin()
def kill_container(id):
    for container in containers:
        if container.id == id:
            container.kill()
    return "Container killed"     

@app.route('/containers')
@cross_origin()
def docker_stats():
    containers = client.containers.list(all=True)
    stats = [{'status': container.status, 'id': container.id, 'name': container.name, 'stats': container.stats(stream=False), 'logs': container.logs(tail=1).decode()} for container in containers]
    return stats



if __name__ in "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
