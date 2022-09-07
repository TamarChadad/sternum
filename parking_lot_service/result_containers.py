class NotAllowedEnterVehicles():
    def __init__(self, number_license, image, description):
        self.number_license = number_license
        self.image = image
        self.description = description

    def get_as_dict(self):
        payload = {
            "number_license": self.number_license,
            "image": self.image,
            "description": self.description
        }
        return payload

class EntrancesAndExitsVehicles():
    def __init__(self, number_license, is_enter_or_exit):
        self.number_license = number_license
        self.is_enter_or_exit = is_enter_or_exit

    def get_as_dict(self):
        payload = {
            "number_license": self.number_license,
            "is_enter_or_exit": self.is_enter_or_exit,
            "description": "The vehicle {} succeeded".format("enter" if self.is_enter_or_exit else "exit")
        }
        return payload
