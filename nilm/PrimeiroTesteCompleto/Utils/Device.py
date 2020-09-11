from Utils.PowerByDate import PowerByDate as pbd
from datetime import datetime
from datetime import timedelta
import numpy as np
import json
import csv


class Device(object):

    def __init__(self, data):
        self.powersByDate = []
        self.chunks = []
        self.idHardware = data['idHardware']
        self.query = data['questao']
        self.answer = data['resposta']
        for powerByDate in data['consumos']:
            self.powersByDate.append(pbd(powerByDate))
        self.workAroundOff()
        self.safe()

    def print(self):
        print('idHardware: ', self.idHardware, end='\n')
        print('questao: ', self.query, end='\n')
        print('resposta: ', self.answer, end='\n')
        for powerByDate in self.powersByDate:
            powerByDate.print()

    def workAroundOff(self):
        self.powersByDate = sorted(self.powersByDate, key=pbd.get_date)
        chunk_head = 0

        for i in range(len(self.powersByDate)-1):
            date_init = datetime.strptime(self.powersByDate[i].get_date(), '%Y-%m-%dT%H:%M:%S')
            date_final = datetime.strptime(self.powersByDate[i+1].get_date(), '%Y-%m-%dT%H:%M:%S')
            if (date_final - date_init) > timedelta(seconds=11):
                self.chunks.append(self.powersByDate[chunk_head:i])
                chunk_head = i

    def safe(self):
        with open('log.csv', mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['id', 'Data', 'Potencia']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for powerByDate in self.powersByDate:
                writer.writerow({'id': self.idHardware, 'Data': powerByDate.get_date(), 'Potencia': powerByDate.get_power()})

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    def power_series(self):
        serie = []
        for powerByDate in self.powersByDate:
            serie.append([powerByDate.get_power()])
        return np.asarray(serie, dtype=np.float32)

    def power_series_g(self):
        serie = []
        for powerByDate in self.powersByDate:
            serie.append(powerByDate.get_power())
        return np.asarray(serie, dtype=np.float32)

    def setPowerByDate(self, powerByDate):
        self.powersByDate = powerByDate

    def power_time(self):
        power =[]
        time = []
        for powerByDate in self.powersByDate:
            power.append(powerByDate.get_power())
            time.append(datetime.strptime(powerByDate.get_date(), '%Y-%m-%dT%H:%M:%S'))
        return power, time

    def get_powerByDate(self):
        return self.powersByDate

    def get_times(self):
        serie = []
        for powerByDate in self.powersByDate:
            serie.append(powerByDate.get_date())
        return serie

    def get_energy(self):
        serie = 0
        for powerByDate in self.powersByDate:
            serie +=powerByDate.get_power()
        return serie