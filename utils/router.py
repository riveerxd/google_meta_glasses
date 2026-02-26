from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

SERVERS = [
    {'url': 'http://localhost:8001', 'type': 'python'},
    {'url': 'http://localhost:8002', 'type': 'javascript'}
]

# ratio 1:3 (JS:Python)
request_count = 0

def get_next_server():
    global request_count
    request_count += 1

    # 1 request to JS, then 3 to Python, repeat
    cycle_pos = (request_count - 1) % 4
    if cycle_pos == 0:
        return SERVERS[1]  # JS
    else:
        return SERVERS[0]  # Python


@app.route('/records', methods=['GET'])
def get_all_records():
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/records"
    else:
        url = f"{server['url']}/getRecords/all"

    try:
        resp = requests.get(url)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/records/<int:id>', methods=['GET'])
def get_record(id):
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/records/{id}"
    else:
        url = f"{server['url']}/getRecord/byId/{id}"

    try:
        resp = requests.get(url)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/records', methods=['POST'])
def create_record():
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/records"
    else:
        url = f"{server['url']}/createRecord"

    try:
        resp = requests.post(url, json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/records/<int:id>', methods=['PUT'])
def update_record(id):
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/records/{id}"
    else:
        url = f"{server['url']}/updateRecord/{id}"

    try:
        resp = requests.put(url, json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


if __name__ == '__main__':
    app.run(port=8000, debug=True)
