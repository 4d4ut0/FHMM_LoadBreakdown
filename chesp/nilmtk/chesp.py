from __future__ import print_function, division
from nilmtk.disaggregate import fhmm_exact
from Utils.HttpRequest import HttpRequest as request
import time as tm
from datetime import datetime as date
from datetime import timedelta
import numpy as np
import copy
import os

time_down = 15
time_down_main = 5
time_down_train = 5
house = '1016'
date_format = '%Y-%m-%dT%H:%M:%S'


def print_time_now():
    print('Tempo atual:', ' {}:{}:{}'.format(date.now().hour, date.now().minute, date.now().second))


def organization(disaggregate_messy, meters_messy):
    disaggregate_messy_new = copy.deepcopy(disaggregate_messy)
    for i, ddv in enumerate(disaggregate_messy.records):
        k = 0
        j = 0
        while k < len(disaggregate_messy.records[i].powersByDate) and j < len(meters_messy[i].powersByDate):
            if disaggregate_messy.records[i].powersByDate[k].get_date() == meters_messy[i].powersByDate[j].get_date():
                disaggregate_messy.records[i].powersByDate[k].idConsumo = meters_messy[i].powersByDate[j].idConsumo
                j += 1
                k += 1
            elif disaggregate_messy.records[i].powersByDate[k].date > meters_messy[i].powersByDate[j].date:
                j += 1
            else:
                k += 1
        lis_del_f = []
        lis_del_v = []
        for o, csm in enumerate(disaggregate_messy.records[i].powersByDate):
            if csm.idConsumo == 0:
                lis_del_f.append(o)
            else:
                lis_del_v.append(o)

        lis_del_f.reverse()
        for d in lis_del_f:
            del disaggregate_messy.records[i].powersByDate[d]

        lis_del_v.reverse()
        for d in lis_del_v:
            del disaggregate_messy_new.records[i].powersByDate[d]

        lis_del_v = []
        for d in range(len(disaggregate_messy_new.records[i].powersByDate)-2):
            date_init = date.strptime(disaggregate_messy_new.records[i].powersByDate[d].get_date(), date_format)
            date_final = date.strptime(disaggregate_messy_new.records[i].powersByDate[d+1].get_date(), date_format)
            if ((date_final - date_init) > timedelta(seconds=60)) \
                    or disaggregate_messy_new.records[i].powersByDate[d+1].get_power() == 0:
                lis_del_v.append(d)

        lis_del_v.reverse()
        for d in lis_del_v:
            del disaggregate_messy_new.records[i].powersByDate[d]

    return disaggregate_messy, disaggregate_messy_new


def combination_meters(new_meter, old_meter=None):
    if old_meter is not None:
        for j, om in enumerate(old_meter):
            nm_in_om = False
            for i, nm in enumerate(new_meter):
                if om.idHardware is nm.idHardware:
                    nm_in_om = True
            if nm_in_om is False:
                new_meter.append(old_meter[j])
    return new_meter


def main():
    # Precisa de dados para testar
    last_get = '/00/00'
    request.setUrl(house, '/23/05/2020', last_get)
    x = request.getTrainAI()
    meters = combination_meters(x.meters())
    if x is None:
        print("Sem estacoes para o treinamento da IA, programa sera finalizado")
        tm.sleep(60 * time_down_main)
    else:
        fhmm = fhmm_exact.FHMM()
        fhmm.nexTrain(x.meters())

        os.system('cls') or None
        print("Treinamento realizado com sucesso")
        print("*************************************")
        none_main = 0
        first_disaggregate = True
        while True:
            if first_disaggregate:
                first_disaggregate = False
            else:
                #request.setUrl(house, '/{}/{}/{}'.format(date.now().day, date.now().month, date.now().year),
                           #'/{}/{}'.format(date.now().hour, date.now().minute))
                print('Pedido de treino: ', '{}/{}/{}'.format((date.now() - timedelta(days=5)).day, date.now().month, date.now().year))
                request.setUrl(house, '/{}/{}/{}'.format((date.now() - timedelta(days=5)).day, date.now().month, date.now().year), '/00/00')
                last_get = '/{}/{}'.format(date.now().hour, date.now().minute)


            x = request.getTrainAI()
            if x is None:
                none_main += 1
                print_time_now()
                print("Tentativa %d: residencia sem estacao principal ativa" % none_main)
                tm.sleep(60 * time_down_main)
                print_time_now()
            else:
                print('Pedido de Desagregacao: ',
                      '{}/{}/{} as '.format(date.now().day, date.now().month, date.now().year), last_get)
                request.setUrl(house, '/{}/{}/{}'.format((date.now()).day, date.now().month, date.now().year), '/00/00')
                last_get = '/{}/{}'.format(date.now().hour, date.now().minute)
                #pegar os pontos dos dipositivos fisicos
                x = request.getTrainAI()
                while x is None:
                    tm.sleep(60 * time_down_train)
                    x = request.getTrainAI()
                nmeters = copy.deepcopy(x.meters())
                meters = combination_meters(nmeters, meters)
                #pegar a main pra desagregacao
                x = request.getDisaggregate()
                while x is None:
                    tm.sleep(60 * time_down_train)
                    x = request.getDisaggregate()
                main = x.main()
                print("Iniciando desagregacao")
                disaggregate = fhmm.nexDisaggregate(main)

                for dv in disaggregate.records:
                    dv.get_energy2()

                disaggregate_fisicos, disaggregate_virtuais = organization(disaggregate, meters)

                request.send_virtuais(disaggregate_virtuais)
                request.send_fisicos(disaggregate_fisicos)

                print_time_now()
                tm.sleep(60 * time_down)
                print_time_now()


if __name__ == "__main__":
    main()

