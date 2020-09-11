import json
from Utils.Device import Device as dv


class PowerRecord(object):

    def __init__(self, data):
        self.records = []
        for record in data['registros']:
            self.records.append(dv(record))
        self.lastTimeStamp = data['dataFinal']

    def print(self):
        for record in self.records:
            record.print()
        print('dataFinal: ', self.lastTimeStamp, end='\n')

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    def main(self):
        return self.records[0]

    def meters(self):
        for i, record in enumerate(self.records):
            if record.idHardware == 'other':
                del self.records[i]
        return self.records[1:]

    def local_meters(self):
        return self.records

    def setRecords(self, records):
        self.records = records
