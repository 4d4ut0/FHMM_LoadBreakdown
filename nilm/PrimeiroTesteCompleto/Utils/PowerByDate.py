import json


class PowerByDate(object):
    def __init__(self, data):
        self.power = data['potencia']
        self.date = data['dataRegistro']

    def get_date(self):
        return self.date

    def get_power(self):
        return self.power

    def diff_power(self, power):
        self.power = self.power - power

    def print(self):
        print('potencia: ', self.power, end='\n')
        print('dataRegistro: ', self.date, end='\n')

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
