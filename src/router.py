from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

SERVERS = [
    {'url': 'http://localhost:8001', 'type': 'python'},
    {'url': 'http://localhost:8002', 'type': 'javascript'}
]

current_server = 0

def get_next_server():
    global current_server
    server = SERVERS[current_server]
    current_server = (current_server + 1) % len(SERVERS)
    return server


@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/tickets"
    else:
        url = f"{server['url']}/getTickets/all"

    try:
        resp = requests.get(url)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/tickets/<int:id>', methods=['GET'])
def get_ticket(id):
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/tickets/{id}"
    else:
        url = f"{server['url']}/getTicket/byId/{id}"

    try:
        resp = requests.get(url)
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/tickets', methods=['POST'])
def create_ticket():
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/tickets"
    else:
        url = f"{server['url']}/createTicket"

    try:
        resp = requests.post(url, json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


@app.route('/tickets/<int:id>', methods=['PUT'])
def update_ticket(id):
    server = get_next_server()

    if server['type'] == 'python':
        url = f"{server['url']}/tickets/{id}"
    else:
        url = f"{server['url']}/updateTicket/{id}"

    try:
        resp = requests.put(url, json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except:
        return jsonify({'error': 'Server nedostupný'}), 503


if __name__ == '__main__':
    app.run(port=8000, debug=True)
