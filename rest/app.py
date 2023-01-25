from flask import Flask, abort, request
import json
import os


app = Flask(__name__)


POSSIBLE_ATTRIBUTES = {
    'username': (type('1'),), 
    'time_on_PC': (type(1),), 
    'email': (type('1'),), 
    'phone_number': (type(1)), 
    'address': (type('1'),),
}


with open(os.path.dirname(__file__) + '/users.json', 'r') as file:
    data = json.load(file)
    USERS = {int(key): value for key, value in data.items()}



def dump_data(data):
    with open(os.path.dirname(__file__) + '/users.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def validate_user(good):
    for key, value in good.items():
        if key not in POSSIBLE_ATTRIBUTES and not isinstance(value, POSSIBLE_ATTRIBUTES.get(key)):
            return False
    return len(POSSIBLE_ATTRIBUTES) == len(good)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/users', methods=['GET'])
def show_all():
    return USERS


@app.route('/users/<id>', methods=['GET'])
def show_one(id):
    return USERS.get(int(id)) if int(id) in USERS else abort(404)


@app.route('/users', methods=['POST'])
def store():
    recieved_data = request.get_json()

    if not validate_user(recieved_data):
        return 406

    if USERS.get(recieved_data['id']):
        return 409

    USERS[recieved_data['id']] = recieved_data

    dump_data(USERS)

    return USERS


def validate_modification(data):
    for key, value in data.items():
        if key not in POSSIBLE_ATTRIBUTES or not isinstance(value, POSSIBLE_ATTRIBUTES.get(key)):
            return False
    return True


@app.route('/users/<id>', methods=['PATCH'])
def modify_user(id):
    recieved_data = request.get_json()

    if not validate_modification(recieved_data):
        return 406

    print(USERS)

    print(id, type(id), '!!!')

    USERS[int(id)] = USERS[int(recieved_data['id'])] | recieved_data

    print(USERS)

    dump_data(USERS)

    return USERS[int(id)]


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        USERS.pop(int(id))
        dump_data(USERS)
    except KeyError:
        return abort(404)


def run():
    app.run(debug=True)

        
if __name__ == '__main__':
    run()
