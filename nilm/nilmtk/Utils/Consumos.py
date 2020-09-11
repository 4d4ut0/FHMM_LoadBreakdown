import json

class Consumos(object):

    def __init__(self):
        self.consumos = []


    def print(self):
        for record in self.consumos:
            record.print()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    def add_fisicos(self, consumos):
        for r in consumos:
            self.consumos.append(r)

    def add_virtuais(self, devices):
        self.consumos = devices
