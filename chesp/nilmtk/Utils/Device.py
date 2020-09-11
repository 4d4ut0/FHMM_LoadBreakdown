from Utils.PowerByDate import PowerByDate as pbd
from datetime import datetime
from datetime import timedelta
import numpy as np
from Utils.math import discrete_integrate as integrate
from Utils.math import function_discrete_integrate as integrate_f
from Utils.Consumo import Consumo as cs
from Utils.math import line_eq, set_period
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
        #for powerByDate in self.powersByDate:
            #powerByDate.print()

    def workAroundOff(self):
        self.powersByDate = sorted(self.powersByDate, key=pbd.get_date)
        chunk_head = 0

        for i in range(len(self.powersByDate)-1):
            date_init = datetime.strptime(self.powersByDate[i].get_date(), '%Y-%m-%dT%H:%M:%S')
            date_final = datetime.strptime(self.powersByDate[i+1].get_date(), '%Y-%m-%dT%H:%M:%S')
            if ((date_final - date_init) > timedelta(seconds=2)) or (np.abs(self.powersByDate[i].get_power() - self.powersByDate[i+1].get_power()) >= 100) :
                self.chunks.append(self.powersByDate[chunk_head:i])
                chunk_head = i


        #self.powersByDate = set_period(self.powersByDate)

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
        return integrate(y = self.power_series_g())

    def get_energy2(self):
        soma = 0
        x1 = 0

        for i,pbd in enumerate(self.powersByDate, 1):
            if i < len(self.powersByDate):
                y1 = self.powersByDate[i-1].get_power()
                x2 = (datetime.strptime(self.powersByDate[i].get_date(), '%Y-%m-%dT%H:%M:%S')
                      - datetime.strptime(self.powersByDate[i-1].get_date(), '%Y-%m-%dT%H:%M:%S')).total_seconds() / 3600
                y2 = self.powersByDate[i].get_power()
                if x1 != x2:
                    f = line_eq(x1, y1, x2, y2)
                    integral = integrate_f(f, x1, x2)
                    self.powersByDate[i].set_consumo(integral/1000)
                    soma += integral
        print("soma: ", soma)
        return soma

    def cut_by_date(self, death_line):
        date_end = datetime.strptime(death_line, '%Y-%m-%dT%H:%M:%S')

        for i, pbd in enumerate(self.powersByDate):
            date_now = datetime.strptime(pbd.get_date(), '%Y-%m-%dT%H:%M:%S')
            if date_now > date_end:
                del self.powersByDate[i:]
                break

    def make2disagregate(self):
        serie = []
        for powerByDate in self.powersByDate:
            serie.append(cs(powerByDate.get_power(), powerByDate.get_consumo(), powerByDate.get_idConsumo()))
        return serie
