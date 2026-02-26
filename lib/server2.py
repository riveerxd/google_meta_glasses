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


@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    data = load_data()
    return make_json_response(data['drinks'])


@app.route('/drinks/<int:id>', methods=['GET'])
def get_drink(id):
    data = load_data()
    for drink in data['drinks']:
        if drink['id'] == id:
            return make_json_response(drink)
    return make_json_response({'error': 'Nápoj nenalezen'}, 404)


@app.route('/drinks', methods=['POST'])
def create_drink():
    data = load_data()
    new_drink = request.get_json()

    if not new_drink.get('name') or not new_drink.get('price'):
        return make_json_response({'error': 'Chybí povinné údaje'}, 400)

    if data['drinks']:
        new_id = max(d['id'] for d in data['drinks']) + 1
    else:
        new_id = 1

    new_drink['id'] = new_id
    data['drinks'].append(new_drink)
    save_data(data)

    return make_json_response(new_drink, 201)


@app.route('/drinks/<int:id>', methods=['PUT'])
def update_drink(id):
    data = load_data()
    update_data = request.get_json()

    for i, drink in enumerate(data['drinks']):
        if drink['id'] == id:
            update_data['id'] = id
            data['drinks'][i] = update_data
            save_data(data)
            return make_json_response(update_data)

    return make_json_response({'error': 'Nápoj nenalezen'}, 404)


if __name__ == '__main__':
    app.run(port=8002, debug=True)
