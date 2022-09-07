
from flask import Flask, request
import json

from parking_lot_service.parking_lot_mechanism import LicensePlatesIdentification

app = Flask(__name__)
parking_lot = None

@app.route('/parkinglot/init', methods=['POST'])
def init_service():
    data = json.loads(request.get_json())
    print("data:", data)
    print("type:", type(data))
    capacity = data["capacity"]
    global parking_lot
    parking_lot = LicensePlatesIdentification(capacity)
    message = "The service up and initial with {}".format(capacity)
    response = app.response_class(response=json.dumps(message),
                                  status=200,
                                  mimetype='application/json')
    return response

@app.route('/parkinglot', methods=['POST'])
def enter_or_exit_from_parking_lot():
    data = json.loads(request.get_json())
    img_path = data['image_path']
    is_enter_or_exit = data['is_enter_or_exit']
    global parking_lot
    message = parking_lot.event_in_parking_lot(img_path, is_enter_or_exit)
    response = app.response_class(response=json.dumps(message.get_as_dict()),
                                  status=200,
                                  mimetype='application/json')

    return response

@app.route('/parkinglot/user', methods=['POST'])
def get_records_from_table():
    data = json.loads(request.get_json())
    name_table = data['name_table']
    name_columns = data['name_columns']
    condition = data['condition']
    message = parking_lot.get_records_from_table(name_table, name_columns, condition)
    response = app.response_class(response=json.dumps(message, indent=1, sort_keys=True, default=str),
                                  status=200,
                                  mimetype='application/json')

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

