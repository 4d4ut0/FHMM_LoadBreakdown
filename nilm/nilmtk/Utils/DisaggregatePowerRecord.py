import json


class DisaggregatePowerRecord(object):

    def __init__(self, records):
        # self.records = [data.records[0]]
        self.records = records

    def print(self):
        for record in self.records:
            record.print()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    def set_other_device(self, dv):
        print(len(self.records))
        times = self.records[0].get_times()
        other_powers = dv.get_powerByDate()


        # igualando numero de amostras na main
        excluidos = []
        for i, other_power in enumerate(other_powers):
            if other_power.get_date() not in times:
                excluidos.append(i)
        excluidos.sort(reverse=True)
        for i in excluidos:
            del other_powers[i]

        # subtraindo os valores desagregados do geral
        for device in self.records:
            print(device.idHardware)
            i = 0
            for power in device.get_powerByDate():
                other_powers[i].diff_power(power.get_power())
                i += 1

        #redefinindo other
        dv.idHardware = 'other'
        dv.setPowerByDate(other_powers)
        self.records.append(dv)