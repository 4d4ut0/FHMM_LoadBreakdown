from __future__ import print_function, division
import os
import copy
import time as tm
import numpy as np
from datetime import timedelta
import Utils.save_manager as sm
from datetime import datetime as date
from nilmtk.disaggregate import fhmm_exact
from Utils.HttpRequest import HttpRequest as rq


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


def cycle_breakdown(house, current_day, current_hour, fhmm):
    meters = sm.save_table(house, current_day, current_hour)
    rq.setUrl(house, current_day, current_hour)
    x = rq.getDisaggregate()
    if (meters is None) or (x is None):
        print('Main ou meters vazios')
    else:
        main = x.main()
        disaggregate = fhmm.nexDisaggregate(main)
        for dv in disaggregate.records:
            dv.idHardware = 'ia_' + dv.idHardware
            dv.get_energy2()
        disaggregate_fisicos, disaggregate_virtuais = organization(disaggregate, meters)
        rq.send_virtuais(disaggregate_virtuais)
        rq.send_fisicos(disaggregate_fisicos)


def cycle_train(house):
    store_data = sm.load_table(house)
    fhmm = fhmm_exact.FHMM()
    fhmm.nexTrain(store_data.meters())
    sm.save_model(house, fhmm)
    return fhmm


def init_model(house, current_day, current_hour):
    fhmm = sm.load_model(house)
    if fhmm is None:
        meters = sm.save_table(house, current_day, current_hour)
        rq.setUrl(house, current_day, current_hour)
        x = rq.getDisaggregate()
        if (meters is None) or (x is None):
            print('Main ou meters vazios')
            return None
        else:
            fhmm = fhmm_exact.FHMM()
            fhmm.nexTrain(meters)
            sm.save_model(house, fhmm)
            return fhmm
    else:
        return fhmm


def main():
    # Inicialization
    house = '1016'
    current_day_string = '{}/{}/{}'.format(date.now().day, date.now().month, date.now().year)
    current_day = date.now()
    new_day = current_day
    current_hour = '/{}/{}'.format(date.now().hour, date.now().minute)
    cycle_time = 15  # in minutes
    fhmm = init_model(house, current_day_string, current_hour)

    while True:
        if (new_day-current_day) >= timedelta(days=1):
            current_day = new_day
            current_day_string = '{}/{}/{}'.format(new_day.day, new_day.month, new_day.year)
            fhmm = cycle_train(house)

        cycle_breakdown(house, current_day_string, current_hour, fhmm)

        current_hour = '/{}/{}'.format(date.now().hour, date.now().minute)
        new_day = date.now()
        tm.sleep(60 * cycle_time)


if __name__ == "__main__":
    main()

