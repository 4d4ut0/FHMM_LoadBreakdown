import json


class Consumo(object):
    def __init__(self, power, consumo, idConsumo):
        self.potenciaDesagregada = power
        self.consumoDesagregado = consumo
        self.idConsumo = idConsumo

    def print(self):
        print('potencia: ', self.potenciaDesagregada, end='\n')
        print('idConsumo: ', self.idConsumo, end='\n')
        print('consumo: ', self.consumoDesagregado, end='\n')

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

