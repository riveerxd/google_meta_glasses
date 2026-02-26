from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

SERVERS = [
    {'url': 'http://localhost:8001', 'type': 'python'},
    {'url': 'http://localhost:8002', 'type': 'javascript'}
]

# ratio 2:3 (Python:JavaScript)
request_count = 0

def get_next_server():
    global request_count
    request_count += 1

    # 2 requests to Python, then 3 to JS, repeat
    cycle_pos = (request_count - 1) % 5
    if cycle_pos < 2:
        return SERVERS[0]  # Python
    else:
        return SERVERS[1]  # JavaScript


@app.route('/protocols', methods=['GET'])
def get_all_protocols():
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/protocols"
    else:
        url = f"{server['url']}/getProtocols/all"

    try:
        resp = requests.get(url, params=request.args)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/protocols/<int:id>', methods=['GET'])
def get_protocol(id):
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/protocols/{id}"
    else:
        url = f"{server['url']}/getProtocol/byId/{id}"

    try:
        resp = requests.get(url)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/protocols', methods=['POST'])
def create_protocol():
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/protocols"
    else:
        url = f"{server['url']}/createProtocol"

    try:
        resp = requests.post(url, json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/protocols/<int:id>', methods=['DELETE'])
def delete_protocol(id):
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/protocols/{id}"
    else:
        url = f"{server['url']}/deleteProtocol/{id}"

    try:
        resp = requests.delete(url)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


if __name__ == '__main__':
    app.run(port=8000, debug=True)
