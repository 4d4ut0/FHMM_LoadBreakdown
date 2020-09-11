from __future__ import print_function, division
from Utils.HttpRequest import HttpRequest as request
from Utils.save_manager import save_device, generate_records2save


house = '1016'

request.setUrl(house, '/02/05/2020', '/00/00')
print('Vai pedir')
x = request.getTrainAI()
print('Pediu')
records2save = generate_records2save(x)
print('Gerou')
for record in records2save:
    dv = record.meters()[0]
    device = dv.idHardware.replace(':', '_')
    print('Gravando o ', device)
    f_time = dv.get_times()[0].replace(':', '_')
    l_time = dv.get_times()[-1].replace(':', '_')

    save_device(house, device, f_time, l_time, record)
