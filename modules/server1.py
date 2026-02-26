from flask import Flask, jsonify, request, make_response
import json

app = Flask(__name__)

def load_data():
    with open('db.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def make_json_response(data, status=200):
    response = make_response(jsonify(data), status)
    response.headers['X-Server-ID'] = 'server1-python'
    return response


@app.route('/protocols', methods=['GET'])
def get_all_protocols():
    data = load_data()
    protocols = data['protocols']

    status_filter = request.args.get('status')
    if status_filter:
        protocols = [p for p in protocols if p['status'] == status_filter]

    return make_json_response(protocols)


@app.route('/protocols/<int:id>', methods=['GET'])
def get_protocol(id):
    data = load_data()
    for protocol in data['protocols']:
        if protocol['id'] == id:
            return make_json_response(protocol)
    return make_json_response({'error': 'Protokol nenalezen'}, 404)


@app.route('/protocols', methods=['POST'])
def create_protocol():
    data = load_data()
    new_protocol = request.get_json()

    if not new_protocol.get('location') or not new_protocol.get('date'):
        return make_json_response({'error': 'Chybí povinné údaje'}, 400)

    if data['protocols']:
        new_id = max(p['id'] for p in data['protocols']) + 1
    else:
        new_id = 1

    new_protocol['id'] = new_id
    data['protocols'].append(new_protocol)
    save_data(data)

    return make_json_response(new_protocol, 201)


@app.route('/protocols/<int:id>', methods=['DELETE'])
def delete_protocol(id):
    data = load_data()

    for i, protocol in enumerate(data['protocols']):
        if protocol['id'] == id:
            deleted = data['protocols'].pop(i)
            save_data(data)
            return make_json_response(deleted)

    return make_json_response({'error': 'Protokol nenalezen'}, 404)


if __name__ == '__main__':
    app.run(port=8001, debug=True)
