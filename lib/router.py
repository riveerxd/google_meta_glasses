from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

SERVERS = [
    {'url': 'http://localhost:8001', 'type': 'javascript'},
    {'url': 'http://localhost:8002', 'type': 'python'}
]

# ratio 1:3 (JS:Python)
request_count = 0

def get_next_server():
    global request_count
    request_count += 1

    # 1 request to JS, then 3 to Python, repeat
    cycle_pos = (request_count - 1) % 4
    if cycle_pos == 0:
        return SERVERS[0]  # JS
    else:
        return SERVERS[1]  # Python


@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    server = get_next_server()

    if server['type'] == 'javascript':
        url = f"{server['url']}/getDrinks/all"
    else:
        url = f"{server['url']}/drinks"

    try:
        resp = requests.get(url)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/drinks/<int:id>', methods=['GET'])
def get_drink(id):
    server = get_next_server()

    if server['type'] == 'javascript':
        url = f"{server['url']}/getDrink/byId/{id}"
    else:
        url = f"{server['url']}/drinks/{id}"

    try:
        resp = requests.get(url)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/drinks', methods=['POST'])
def create_drink():
    server = get_next_server()

    if server['type'] == 'javascript':
        url = f"{server['url']}/createDrink"
    else:
        url = f"{server['url']}/drinks"

    try:
        resp = requests.post(url, json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/drinks/<int:id>', methods=['PUT'])
def update_drink(id):
    server = get_next_server()

    if server['type'] == 'javascript':
        url = f"{server['url']}/updateDrink/{id}"
    else:
        url = f"{server['url']}/drinks/{id}"

    try:
        resp = requests.put(url, json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


if __name__ == '__main__':
    app.run(port=8000, debug=True)
