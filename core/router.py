from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

SERVERS = [
    {'url': 'http://localhost:8001', 'type': 'javascript'},
    {'url': 'http://localhost:8002', 'type': 'python'}
]

current_server = 0

def get_next_server():
    global current_server
    server = SERVERS[current_server]
    current_server = (current_server + 1) % len(SERVERS)
    return server


@app.route('/animals', methods=['GET'])
def get_all_animals():
    server = get_next_server()

    if server['type'] == 'javascript':
        url = f"{server['url']}/getAnimals/all"
    else:
        url = f"{server['url']}/animals"

    try:
        resp = requests.get(url)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/animals/<int:id>', methods=['GET'])
def get_animal(id):
    server = get_next_server()

    if server['type'] == 'javascript':
        url = f"{server['url']}/getAnimal/byId/{id}"
    else:
        url = f"{server['url']}/animals/{id}"

    try:
        resp = requests.get(url)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/animals', methods=['POST'])
def create_animal():
    server = get_next_server()

    if server['type'] == 'javascript':
        url = f"{server['url']}/createAnimal"
    else:
        url = f"{server['url']}/animals"

    try:
        resp = requests.post(url, json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    server = get_next_server()

    if server['type'] == 'javascript':
        url = f"{server['url']}/updateAnimal/{id}"
    else:
        url = f"{server['url']}/animals/{id}"

    try:
        resp = requests.put(url, json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


if __name__ == '__main__':
    app.run(port=8000, debug=True)
