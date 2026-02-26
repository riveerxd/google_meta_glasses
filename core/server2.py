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
    response.headers['X-Server-ID'] = 'server2-python'
    return response


@app.route('/animals', methods=['GET'])
def get_all_animals():
    data = load_data()
    return make_json_response(data['animals'])


@app.route('/animals/<int:id>', methods=['GET'])
def get_animal(id):
    data = load_data()
    for animal in data['animals']:
        if animal['id'] == id:
            return make_json_response(animal)
    return make_json_response({'error': 'Zvíře nenalezeno'}, 404)


@app.route('/animals', methods=['POST'])
def create_animal():
    data = load_data()
    new_animal = request.get_json()

    if not new_animal.get('name') or not new_animal.get('species'):
        return make_json_response({'error': 'Chybí povinné údaje'}, 400)

    if data['animals']:
        new_id = max(a['id'] for a in data['animals']) + 1
    else:
        new_id = 1

    new_animal['id'] = new_id
    data['animals'].append(new_animal)
    save_data(data)

    return make_json_response(new_animal, 201)


@app.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    data = load_data()
    update_data = request.get_json()

    for i, animal in enumerate(data['animals']):
        if animal['id'] == id:
            update_data['id'] = id
            data['animals'][i] = update_data
            save_data(data)
            return make_json_response(update_data)

    return make_json_response({'error': 'Zvíře nenalezeno'}, 404)


if __name__ == '__main__':
    app.run(port=8002, debug=True)
