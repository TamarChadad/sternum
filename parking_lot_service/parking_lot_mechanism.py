import json
import requests
import logging
from parking_lot_service.data_base import DataBase
from parking_lot_service.result_containers import EntrancesAndExitsVehicles, NotAllowedEnterVehicles


class LicensePlatesIdentification(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.current_count = 0
        self.db = DataBase()
        self.logger = self.config_logger()

    def get_license_plates_from_image(self, img_path):
        payload = {'isOverlayRequired': True,
                   'apikey': 'helloworld',
                   'language': 'eng'}
        try:
            with open(img_path, 'rb') as file:
                response = requests.post('https://api.ocr.space/parse/image',
                                         files={img_path: file},
                                         data=payload,
                                         verify=False)
                if response.status_code != 200:
                    self.logger.warning("The request ocr.space api Failed!!")
                    return None
        except Exception as e:
            self.logger.error('The error: {}'.format(e))
            assert False, 'The error: {}'.format(e)
        result = response.content.decode()
        result = json.loads(result)
        try:
            license_string = result["ParsedResults"][0]["ParsedText"]
            return self.__get_only_digits_from_license(license_string)
        except:
            self.logger.warning("The OCR.SPACE api did not success to recognize text")
            return None

    def event_in_parking_lot(self, img, is_enter_or_exit):
        number_license = self.get_license_plates_from_image(img)
        if not is_enter_or_exit:  # if the vehicle exit from parking lot
            result = EntrancesAndExitsVehicles(number_license=number_license, is_enter_or_exit=False)
            self.current_count -= 1
        elif self.current_count < self.capacity:  # If there is free parking
            is_valid_license = self.validate_license_plates(number_license)
            if not is_valid_license and number_license is None:  # if the license invalid
                result = NotAllowedEnterVehicles(number_license=number_license, image=img, description="The system dont success recognize license")
            elif not is_valid_license:
                result = NotAllowedEnterVehicles(number_license=number_license, image=img, description="The license is invalid")
            else:  # The vehicle succeeded enter to parking lot
                result = EntrancesAndExitsVehicles(number_license=number_license, is_enter_or_exit=True)
                self.current_count += 1
        else:  # The parking lot is full
            result = NotAllowedEnterVehicles(number_license=number_license, image=img,
                                             description='The parking lot is full')

        self.insert_event_to_db(result)
        return result

    def get_records_from_table(self, name_table, name_columns, condition):
        try:
            data = self.db.execute_db_cmd('''SELECT {name_columns} FROM {name_table} '''.format(name_columns=name_columns,
                                       name_table=name_table,
                                       condition="WHERE {}".format(condition) if condition!="" else "")).fetchall()
            self.logger.info("The data selected succeeded")
        except Exception as e:
            self.logger.error("There is error in select data: {}".format(e))
        return [tuple(row) for row in data]

    def insert_event_to_db(self, result):
        try:
            if isinstance(result, NotAllowedEnterVehicles):
                self.db.execute_db_cmd('''INSERT INTO NotAllowedEnterVehicles (NumberLicense, [Image], [Description]) VALUES ({number_license}, '{image}', '{description}')'''
                                       .format(number_license=None if result.number_license is None else "'{}'".format(result.number_license),
                                               image=result.image,
                                               description=result.description))

            else:
                self.db.execute_db_cmd('''INSERT INTO EntrancesAndExitsVehicles (NumberLicense, IsEnterOrExit) VALUES ( '{number_licens}', {is_enter_or_exit})'''
                                       .format(number_licens=result.number_license,
                                               is_enter_or_exit=int(result.is_enter_or_exit)))
                self.logger.info("The result saved in DB")
        except Exception as e:
            self.logger.error("There is error in save data in DB: {}".format(e))

    @staticmethod
    def validate_license_plates(number_license):
        if number_license is None:
            return False
        last_two_digits = int(number_license[-2:])
        if last_two_digits in [25, 26]:
            return True
        elif (last_two_digits >= 85 and last_two_digits <= 89) or last_two_digits == 00:
            return False
        if len(number_license) == 7 and last_two_digits % 10 in [0, 5]:
            return False
        return True

    @staticmethod
    def __get_only_digits_from_license(license_string):
        license_digits = ""
        for char in license_string:
            if char.isdigit():
                license_digits += char
        return license_digits

    @staticmethod
    def config_logger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s >>>> %(levelname)s   %(message)s')
        handler = logging.FileHandler('../parking_lot.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
