import json


class PowerByDate(object):
    def __init__(self, data):
        self.power = data['potencia']
        self.date = data['dataRegistro']
        self.consumo = 0
        self.idConsumo = data['idConsumo']

    def get_date(self):
        return self.date

    def get_power(self):
        return self.power

    def get_consumo(self):
        return self.consumo

    def get_idConsumo(self):
        return self.idConsumo

    def diff_power(self, power):
        self.power = self.power - power

    def set_consumo(self, consumo):
        self.consumo = consumo

    def date_is_not_zero_minute(self):
        return self.date[-2:] != '00'

    def print(self):
        print('potencia: ', self.power, end='\n')
        print('dataRegistro: ', self.date, end='\n')
        print('consumo: ', self.consumo, end='\n')
        print('idConsumo: ', self.idConsumo, end='\n')

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
