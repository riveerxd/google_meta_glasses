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


@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    data = load_data()
    return make_json_response(data['tickets'])


@app.route('/tickets/<int:id>', methods=['GET'])
def get_ticket(id):
    data = load_data()
    for ticket in data['tickets']:
        if ticket['id'] == id:
            return make_json_response(ticket)
    return make_json_response({'error': 'Vstupenka nenalezena'}, 404)


@app.route('/tickets', methods=['POST'])
def create_ticket():
    data = load_data()
    new_ticket = request.get_json()

    if not new_ticket.get('name') or not new_ticket.get('table'):
        return make_json_response({'error': 'Chybí povinné údaje'}, 400)

    if data['tickets']:
        new_id = max(t['id'] for t in data['tickets']) + 1
    else:
        new_id = 1

    new_ticket['id'] = new_id
    data['tickets'].append(new_ticket)
    save_data(data)

    return make_json_response(new_ticket, 201)


@app.route('/tickets/<int:id>', methods=['PUT'])
def update_ticket(id):
    data = load_data()
    update_data = request.get_json()

    for i, ticket in enumerate(data['tickets']):
        if ticket['id'] == id:
            update_data['id'] = id
            data['tickets'][i] = update_data
            save_data(data)
            return make_json_response(update_data)

    return make_json_response({'error': 'Vstupenka nenalezena'}, 404)


if __name__ == '__main__':
    app.run(port=8001, debug=True)
