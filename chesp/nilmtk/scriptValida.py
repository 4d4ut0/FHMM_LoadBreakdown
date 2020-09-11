from __future__ import print_function, division
from nilmtk.disaggregate import fhmm_exact
from Utils.HttpRequest import HttpRequest as request
import matplotlib.pyplot as pl
import time as tm
from Utils.Consumos import Consumos as cs
from datetime import datetime as date
import copy
import os

inicio_total = tm.time()
none_main = 0
time_down = 15
time_down_main = 5
time_down_train = 5

house = '1016'


#Precisa de dados para testar
request.setUrl(house, '/08/05/2020', '/00/00')
inicio_get = tm.time()
x = request.getTrainAI()
fim_get = tm.time()
if x is None:
    print("Sem estacoes para o treinamento da IA, programa sera finalizado")
    exit()
else:
    inicio_tr = tm.time()
    fhmm = fhmm_exact.FHMM()
    meters = copy.deepcopy(x.meters())

    fhmm.nexTrain(x.meters())
    fim_tr = tm.time()

    os.system('cls') or None
    print("Treinamento realizado com sucesso")
    print("*************************************")
    while True:
        request.setUrl(house, '/{}/{}/{}'.format(date.now().day, date.now().month, date.now().year),
                       '/{}/{}'.format(date.now().hour, date.now().minute))
        energys = []
        for dv in x.meters():
            energys.append((dv.idHardware, dv.get_energy2(), len(dv.powersByDate)))
            q, w = dv.power_time()

        y = request.getDisaggregate()
        if y is None:
            none_main += 1
            print("Tentativa %d: residencia sem estacao principal cadastrada" % none_main)
            tm.sleep(60 * 5)
        else:
            print("Iniciando desagregacao")
            main = y.main()
            inicio_dis = tm.time()
            disaggregate = fhmm.nexDisaggregate(main)
            fim_dis = tm.time()

            power, time = main.power_time()
            a = power
            b = time
            print(power[0], time[0])

            '''
            #Filtro de dados
            c, d = signal.butter(2, 0.8, 'low')
            output = signal.filtfilt(c, d, power)
            pl.plot(time, output, 'r', label='filtered')
            pl.legend()
            

            pl.plot(time, power, 'b', label='normal')
            pl.gcf().autofmt_xdate()
            pl.title(main.idHardware)
            pl.show()
            '''

            print("Get: ", fim_get - inicio_get)
            print("Treinamento: ", fim_tr - inicio_tr)
            print("Desagregacao: ", fim_dis - inicio_dis)

            #gambiarra
            '''
            for dv in disaggregate.records:
                dv.powersByDate.reverse()
                print(len(dv.powersByDate))
                while len(dv.powersByDate) > 500:
                    del dv.powersByDate[len(dv.powersByDate)-1]
                print(len(dv.powersByDate))
            '''
            #fim da gambiarra


            print("\n\n\n\n\n\n---------------------------------------------")
            i = 0

            for dv in disaggregate.records:
                energys.append((dv.idHardware, dv.get_energy2(), len(dv.powersByDate)))
                power, time = dv.power_time()
                pl.plot(b, a, 'b', w, q, 'g', time, power, 'r')
                pl.gcf().autofmt_xdate()
                pl.title(dv.idHardware)
                #pl.show()
                i += 1
            print("\n\n\n\n\n\n---------------------------------------------")

            for dv in energys:
                print("Medidor ", dv[0], ": ", dv[1], " - ", dv[2])
                print("Consumo medio diario: ", dv[1]/dv[2])

            for i, ddv in enumerate(disaggregate.records):
                k = 0
                j = 0
                while k < len(disaggregate.records[i].powersByDate) and j < len(meters[i].powersByDate):
                    if disaggregate.records[i].powersByDate[k].get_date() == meters[i].powersByDate[j].get_date():
                        disaggregate.records[i].powersByDate[j].idConsumo = meters[i].powersByDate[j].idConsumo
                        j += 1
                        k += 1
                    elif disaggregate.records[i].powersByDate[k].date > meters[i].powersByDate[j].date:
                        j += 1
                    else:
                        k += 1
                lis_del = []
                for o, csm in enumerate(disaggregate.records[i].powersByDate):
                    if csm.idConsumo == 0:
                        lis_del.append(o)

                lis_del.reverse()
                for d in lis_del:
                    del disaggregate.records[i].powersByDate[d]

            envio = cs()
            for dv in disaggregate.records:
                envio.add(dv.make2disagregate())
            request.postDisaggregate(envio)
            tm.sleep(60*time_down)

