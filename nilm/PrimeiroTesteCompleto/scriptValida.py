from __future__ import print_function, division
from nilmtk.disaggregate import fhmm_exact
from Utils.HttpRequest import HttpRequest as request
import matplotlib.pyplot as pl
import time as tm
from datetime import date
import os

none_main = 0

#Precisa de dados para testar
request.setUrl('1016', '/08/04/2020')
x = request.getTrainAI()

if x is None:
    print("Sem estacoes para o treinamento da IA, programa sera finalizado")
    exit()
else:
    fhmm = fhmm_exact.FHMM()
    fhmm.nexTrain(x.meters())

    energys = []
    for dv in x.meters():
       energys.append((dv.idHardware, dv.get_energy()))

    os.system('cls') or None
    print("Treinamento realizado com sucesso")
    print("*************************************")
    while True:
        #request.setUrl('1016', '/{}/{}/{}'.format(date.today().day, date.today().month, date.today().year))
        y = request.getDisaggregate()
        if y is None:
            if none_main > 10:
                print("Programa sera finalizado por falta de estacao principal")
                exit()
            else:
                none_main += 1
                print("Tentativa %d: residencia sem estacao principal cadastrada" % none_main)
        else:
            print("Iniciando desagregacao")
            main = y.main()
            disaggregate = fhmm.nexDisaggregate(main)

            power, time = main.power_time()
            a = power
            b = time
            print(power[0], time[0])
            pl.plot(time, power, 'b')
            pl.gcf().autofmt_xdate()
            pl.title(main.idHardware)
            pl.show()
            disaggregate.set_other_device(main)
            print("\n\n\n\n\n\n---------------------------------------------")
            i = 0
            for dv in disaggregate.records:
                energys.append((dv.idHardware, dv.get_energy()))
                power, time = dv.power_time()
                pl.plot(b, a, 'b', time, power, 'r')
                pl.gcf().autofmt_xdate()
                pl.title(dv.idHardware)
                pl.show()
                i += 1
            print("\n\n\n\n\n\n---------------------------------------------")

            for energy in energys:
                print("O hardware ", energy[0], " tem energia = ", energy[1])

            request.postDisaggregate(disaggregate)
            #tm.sleep(60*30)
            exit()
