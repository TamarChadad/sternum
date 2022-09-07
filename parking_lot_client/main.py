import json
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s >>>> %(levelname)s   %(message)s')
handler = logging.FileHandler('../parking_lot.log')
handler.setFormatter(formatter)
logger.addHandler(handler)

URI = 'http://localhost:5000/parkinglot'

def invoke_request(route="", payload=None):
    url = URI + route
    payload = json.dumps(payload, ensure_ascii=False)
    resp = requests.post(url=url, json=payload)
    return resp

def initial_capacity_of_parking_lot(capacity_parking_lot):
    payload = {"capacity": capacity_parking_lot}
    try:
        resp =invoke_request('/init', payload)
        if resp.status_code == 200:
            logger.info("The service up")
    except Exception as e:
        logger.error("The service down. Error:{}".format(e))
        print("The service down!")
        exit()

def enter_or_exit_vehicle_to_parking_lot(image_path, is_enter_or_exit):
    payload = {"image_path": image_path, "is_enter_or_exit": is_enter_or_exit}
    resp = invoke_request(payload=payload)
    if resp.status_code == 200:
        resp = json.loads(resp.content)
        logger.debug(resp['description'])
        print(resp['description'])
    else:
        print("There is problem in your input")
        logger.error("Status code = {}".format(resp.status_code))

def get_records_from_db():
    columns_tables = {
        1: {"name_table": "EntrancesAndExitsVehicles", "columns": ["*", "[NumberLicense]", "[IsEnterOrExit]", "[Timestamp]" ]},
        2: {"name_table": "NotAllowedEnterVehicles", "columns": ["*", "[NumberLicense]", "[Image]", "[Description]", "[Timestamp]" ]}
    }
    num_table = int(input(" Enter 1 for select from {} table\n Enter 2 for select from {} table\n".format(columns_tables[1]['name_table'],columns_tables[2]['name_table'])))
    columns = columns_tables[num_table]['columns']
    message = "Enter 1 for all columns\n"
    for i in range(1, len(columns)):
        message += "Enter {} for {}\n".format(i+1, columns[i])

    num_column = int(input(message))
    condition = input("Add condition (for without condition enter Enter): ")
    payload = {"name_table": columns_tables[num_table]['name_table'],
               "name_columns": columns_tables[num_table]['columns'][num_column-1],
               "condition": condition}
    try:
        resp = invoke_request('/user', payload)
        data = json.loads(resp.content)
    except Exception as e:
        logger.error("The error: {}".format(e))
        print("There is problem in the service")
        return

    if columns_tables[num_table]['columns'][num_column-1] == "*":
        if num_table == 1:
            print("NumberLicense\tIsEnterOrExit\t")
        else:
            print("NumberLicense\tImage\tDescription\t")
    else:
        print(columns_tables[num_table]['columns'][num_column-1])
    for row in data:
        for col in row:
            print(str(col) + '\t', end="")
        print('\n')

def main():
    capacity = int(input("Enter capacity for parking lot: "))
    initial_capacity_of_parking_lot(capacity_parking_lot=capacity)
    while True:
        which_action = (input(" Enter 1 for exit vehicle\n Enter 2 for enter vehicle\n Enter 3 for view report\n Enter 4 for exit"))
        try:
            which_action = int(which_action)
        except:
            continue
        if which_action in [1, 2]:
            image_path = input("Enter image path to enter Example: ../images/car_end_56.png")
            enter_or_exit_vehicle_to_parking_lot(image_path, bool(which_action - 1))
        elif which_action == 3:
            get_records_from_db()
        elif which_action == 4:
            exit()

if __name__ == "__main__":
    main()
