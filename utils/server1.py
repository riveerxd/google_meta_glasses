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


@app.route('/records', methods=['GET'])
def get_all_records():
    data = load_data()
    return make_json_response(data['records'])


@app.route('/records/<int:id>', methods=['GET'])
def get_record(id):
    data = load_data()
    for record in data['records']:
        if record['id'] == id:
            return make_json_response(record)
    return make_json_response({'error': 'Záznam nenalezen'}, 404)


@app.route('/records', methods=['POST'])
def create_record():
    data = load_data()
    new_record = request.get_json()

    if not new_record.get('client') or not new_record.get('date'):
        return make_json_response({'error': 'Chybí povinné údaje'}, 400)

    if data['records']:
        new_id = max(r['id'] for r in data['records']) + 1
    else:
        new_id = 1

    new_record['id'] = new_id
    data['records'].append(new_record)
    save_data(data)

    return make_json_response(new_record, 201)


@app.route('/records/<int:id>', methods=['PUT'])
def update_record(id):
    data = load_data()
    update_data = request.get_json()

    for i, record in enumerate(data['records']):
        if record['id'] == id:
            update_data['id'] = id
            data['records'][i] = update_data
            save_data(data)
            return make_json_response(update_data)

    return make_json_response({'error': 'Záznam nenalezen'}, 404)


if __name__ == '__main__':
    app.run(port=8001, debug=True)
